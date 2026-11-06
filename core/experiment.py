"""Modelo determinístico para os experimentos virtuais do trabalho da UEMG."""
from dataclasses import dataclass
from math import floor

from core.energy import energy_kwh
from core.thermal import AMBIENTE_C, update_temperature
from models.computer import Computer

PC = Computer()
AUXILIARY_W = {"Placa mãe e VRM (agrupados)": 25, "RAM": 6, "SSD NVMe": 3, "Ventoinhas": 6}
ACTIVITIES = {
    "Escritório": (.70, .35),
    "Computação intensiva": (1.0, .35),
    "Renderização gráfica": (.55, 1.0),
}
COOLING = {
    "Adequada": (1.0, 1.0),
    "Limitada": (1.4, 1.65),
    "Insuficiente": (2.0, 2.6),
}
THERMAL_LIMITS = (84, 83)
TEST_SECONDS = 180


@dataclass(frozen=True)
class Chip:
    idle_w: float
    max_w: float
    max_ghz: float
    idle_v: float
    peak_v: float
    limit_c: float
    conduction_k_w: float
    convection_k_w: float
    capacity_j_k: float

    def reading(self, demand, temperature, clock_ratio=1.0, offset_v=0.0, cap_w=None):
        target_ratio = (0.35 + .65 * demand) * clock_ratio
        throttle = max(.35, 1 - .032 * max(0, temperature - self.limit_c))
        ratio = target_ratio * throttle
        voltage = max(.5, self.idle_v + (self.peak_v - self.idle_v) * ratio + offset_v)
        # Capacitância efetiva calibrada pela potência dinâmica de referência.
        capacitance = (self.max_w - self.idle_w) / (self.peak_v**2 * self.max_ghz * 1e9)
        dynamic = demand * capacitance * voltage**2 * ratio * self.max_ghz * 1e9
        if cap_w is not None and dynamic > cap_w - self.idle_w:
            ratio *= (cap_w - self.idle_w) / dynamic
            dynamic = cap_w - self.idle_w
        return voltage, ratio, self.idle_w + dynamic, throttle < 1

    def next_temperature(self, temperature, heat_w, cooling):
        contact, airflow = cooling
        resistance = self.conduction_k_w * contact + self.convection_k_w * airflow
        target = AMBIENTE_C + .05 * sum(AUXILIARY_W.values()) + resistance * heat_w
        return update_temperature(temperature, target, 1, resistance * self.capacity_j_k)


CPU = Chip(PC.cpu.IDLE_W, PC.cpu.MAX_W, 4.2, .78, 1.25, THERMAL_LIMITS[0], .13, .30, 85)
GPU = Chip(PC.gpu.IDLE_W, PC.gpu.MAX_W, 2.2, .70, 1.05, THERMAL_LIMITS[1], .07, .18, 130)


def simulate(activity, segments, cooling="Adequada", start=None, offset_mv=0, clock_ratio=1.0, cap_w=None):
    """Cada amostra representa um segundo; demanda e potência são constantes nesse intervalo."""
    cpu_temp, gpu_temp = start or (AMBIENTE_C, AMBIENTE_C)
    load_cpu, load_gpu = ACTIVITIES[activity]
    cooling_params = COOLING[cooling]
    accumulated_kwh = 0.0
    fault_exposure = 0.0
    seconds = 0
    crashed = False
    rows = []
    for load, duration in segments:
        cpu_demand, gpu_demand = load_cpu * load / 100, load_gpu * load / 100
        for _ in range(duration):
            cpu_v, cpu_ratio, cpu_w, cpu_throttle = CPU.reading(
                cpu_demand, cpu_temp, clock_ratio, offset_mv / 1000, cap_w
            )
            gpu_v, gpu_ratio, gpu_w, gpu_throttle = GPU.reading(gpu_demand, gpu_temp)
            deficit = max(0, .61 + .51 * cpu_ratio - cpu_v)
            if not crashed:
                fault_exposure += 18 * deficit
                crashed = fault_exposure >= 5
            if crashed:
                cpu_ratio = gpu_ratio = 0
                cpu_w, gpu_w = CPU.idle_w, GPU.idle_w
                cpu_throttle = gpu_throttle = False
            total_w = cpu_w + gpu_w + sum(AUXILIARY_W.values())
            # Trabalho útil relativo ao máximo da atividade com ambos os clocks máximos.
            performance = 100 * (cpu_demand * cpu_ratio + gpu_demand * gpu_ratio) / (load_cpu + load_gpu)
            if not crashed:
                performance *= max(0, 1 - 8 * deficit)
            cpu_temp = CPU.next_temperature(cpu_temp, cpu_w, cooling_params)
            gpu_temp = GPU.next_temperature(gpu_temp, gpu_w, cooling_params)
            accumulated_kwh += energy_kwh(total_w, 1)
            seconds += 1
            rows.append({
                "Tempo (s)": seconds, "Carga solicitada (%)": load,
                "CPU solicitada (%)": 100 * cpu_demand, "GPU solicitada (%)": 100 * gpu_demand,
                "Potência total (W)": total_w, "CPU (W)": cpu_w, "GPU (W)": gpu_w,
                "CPU (°C)": cpu_temp, "GPU (°C)": gpu_temp,
                "CPU (V)": cpu_v, "GPU (V)": gpu_v,
                "CPU (A)": cpu_w / cpu_v, "GPU (A)": gpu_w / gpu_v,
                "CPU (GHz)": CPU.max_ghz * cpu_ratio, "GPU (GHz)": GPU.max_ghz * gpu_ratio,
                "Desempenho (%)": performance, "Energia (Wh)": accumulated_kwh * 1000,
                "CPU limitada": cpu_throttle, "GPU limitada": gpu_throttle,
                "Erros simulados": min(5, floor(fault_exposure)), "Travou": crashed,
            })
    return rows


def initial_temperatures(rows):
    last = rows[-1]
    return last["CPU (°C)"], last["GPU (°C)"]


def summarize(rows):
    """Médias sobre a execução toda, incluindo períodos de falha."""
    fields = ("Potência total (W)", "CPU (V)", "CPU (GHz)", "GPU (GHz)", "Desempenho (%)")
    summary = {field: sum(row[field] for row in rows) / len(rows) for field in fields}
    summary["Pico CPU (°C)"] = max(row["CPU (°C)"] for row in rows)
    summary["Pico GPU (°C)"] = max(row["GPU (°C)"] for row in rows)
    summary["Desempenho por W"] = summary["Desempenho (%)"] / summary["Potência total (W)"]
    summary["Primeira limitação (s)"] = next(
        (row["Tempo (s)"] for row in rows if row["CPU limitada"] or row["GPU limitada"]), None
    )
    summary["Erros simulados"] = rows[-1]["Erros simulados"]
    summary["Travou"] = rows[-1]["Travou"]
    return summary
