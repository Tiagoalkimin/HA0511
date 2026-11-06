"""Três estados da mesma tarefa em um modelo simulado de computador."""
from dataclasses import dataclass

from core.energy import compute_power, cost_from_kwh, energy_kwh, expected_power_range
from core.thermal import AMBIENTE_C, target_temperature, update_temperature
from models.computer import Computer

HOURS_PER_DAY = 8
DAYS_PER_MONTH = 30
TARIFF = 0.90
THERMAL_INTERVAL_S = 180
WASTE_W = 90.0
CPU_RANGE = (8, 18)
GPU_RANGE = (2, 8)
BALANCED_LOAD_FACTOR = 0.85
ANOMALY_MARGIN = 1.15


@dataclass(frozen=True)
class Reading:
    power_w: float
    temperature_c: float
    monthly_kwh: float
    monthly_cost: float


class QuickDemo:
    def __init__(self):
        self.computer = Computer()
        _, expected_max = expected_power_range(self.computer, CPU_RANGE, GPU_RANGE)
        self.alert_limit_w = expected_max * ANOMALY_MARGIN
        self.initial = self._reading(AMBIENTE_C + 5, 0)
        self.waste = None
        self.optimized = None

    def _reading(self, previous_temp, waste_w):
        cpu_util = sum(CPU_RANGE) / 2 * BALANCED_LOAD_FACTOR
        gpu_util = sum(GPU_RANGE) / 2 * BALANCED_LOAD_FACTOR
        power = compute_power(self.computer, cpu_util, gpu_util, waste_w)["total_w"]
        target = target_temperature(
            power, self.computer.max_power_w(), self.computer.thermal_reference_c
        )
        temperature = update_temperature(
            previous_temp, target, THERMAL_INTERVAL_S, self.computer.thermal_tau_s
        )
        monthly_kwh = energy_kwh(power, HOURS_PER_DAY * DAYS_PER_MONTH * 3600)
        return Reading(power, temperature, monthly_kwh, cost_from_kwh(monthly_kwh, TARIFF))

    def has_anomaly(self, reading):
        return reading.power_w > self.alert_limit_w

    def inject_waste(self):
        if self.waste is None:
            self.waste = self._reading(self.initial.temperature_c, WASTE_W)

    def optimize(self):
        if self.waste is not None and self.optimized is None and self.has_anomaly(self.waste):
            self.optimized = self._reading(self.waste.temperature_c, 0)
