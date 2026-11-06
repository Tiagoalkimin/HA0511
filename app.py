import streamlit as st

from core.experiment import (
    ACTIVITIES, AUXILIARY_W, COOLING, TEST_SECONDS, THERMAL_LIMITS,
    initial_temperatures, simulate, summarize,
)

st.set_page_config(page_title="EnergyLens | Laboratório virtual", page_icon="⚡", layout="wide")

POWER = "Potência total (W)"
PERFORMANCE = "Desempenho (%)"
TIME = "Tempo (s)"
TEMPS = ["CPU (°C)", "GPU (°C)"]
STEPS = ("1 · Referência", "2 · Demanda", "3 · Refrigeração", "4 · Eficiência")


def number(value, decimals=1):
    return f"{value:.{decimals}f}".replace(".", ",")


def indicators(items):
    for column, (label, value) in zip(st.columns(len(items)), items):
        column.metric(label, value, border=True)


def comparison(summaries, fields):
    rows = []
    for name, summary in summaries.items():
        row = {"Cenário": name}
        for field, digits in fields:
            value = summary[field]
            row[field] = "Sem limitação" if value is None else number(value, digits)
        row["Estado"] = (
            "Travamento simulado" if summary["Travou"]
            else "Com limitação térmica" if summary["Primeira limitação (s)"] is not None
            else "Com erros simulados" if summary["Erros simulados"]
            else "Estável no teste"
        )
        rows.append(row)
    st.table(rows)


st.title("⚡ EnergyLens")
st.caption("UEMG · Engenharia de Computação · Simulação virtual com parâmetros ilustrativos")
st.markdown("**Quando aumentar a potência deixa de entregar mais desempenho?**")
step = st.radio("Etapa da investigação", STEPS, horizontal=True)
controls = st.columns(2)
activity = controls[0].selectbox("Atividade simulada", ACTIVITIES.keys(), index=1)
load = controls[1].radio("Carga solicitada no teste", (25, 50, 75, 100), index=3,
                         format_func=lambda value: f"{value}%", horizontal=True)

normal = simulate(activity, [(25, 90)])
initial = normal[-1]
start = initial_temperatures(normal)
focus = "GPU" if activity == "Renderização gráfica" else "CPU"

if step == STEPS[0]:
    st.header("O mesmo computador como referência")
    st.write("Observe 90 segundos simulados com demanda de 25% e refrigeração adequada.")
    indicators([
        ("Potência total", f"{number(initial[POWER])} W"),
        ("Temperatura da CPU", f"{number(initial[TEMPS[0]])} °C"),
        ("Temperatura da GPU", f"{number(initial[TEMPS[1]])} °C"),
        ("Energia em 90 s", f"{number(initial['Energia (Wh)'], 2)} Wh"),
    ])
    st.caption(f"Utilização solicitada de CPU: {number(initial['CPU solicitada (%)'])}%. "
               f"GPU: {number(initial['GPU solicitada (%)'])}%. Temperatura inicial do modelo: 24 °C.")
    st.line_chart(normal, x=TIME, y="Energia (Wh)", height=220)
    with st.expander("Potência por componente e valores elétricos"):
        st.table([{"Componente": name, "Potência (W)": number(value)} for name, value in
                  {"CPU": initial["CPU (W)"], "GPU": initial["GPU (W)"], **AUXILIARY_W}.items()])
        st.table([{"Componente": name, "Tensão (V)": number(initial[f"{name} (V)"], 3),
                   "Corrente (A)": number(initial[f"{name} (A)"]),
                   "Clock (GHz)": number(initial[f"{name} (GHz)"], 2)}
                  for name in ("CPU", "GPU")])
        st.caption("Corrente no circuito modelado de cada chip. A parcela da placa mãe inclui o VRM e outros consumos agrupados.")

elif step == STEPS[1]:
    st.header("Mais demanda, mais dissipação")
    levels = tuple(level for level in (25, 50, 75, 100) if level <= load)
    ramp = simulate(activity, [(level, 45) for level in levels], start=start)
    last = ramp[-1]
    st.caption("Cada nível dura 45 segundos simulados. A temperatura ao fim de um nível passa para o próximo.")
    indicators([
        ("Potência final", f"{number(last[POWER])} W"),
        (f"Corrente da {focus}", f"{number(last[f'{focus} (A)'])} A"),
        (f"Clock da {focus}", f"{number(last[f'{focus} (GHz)'], 2)} GHz"),
        ("Calor gerado no modelo", f"{number(last[POWER])} W térmicos"),
    ])
    left, right = st.columns(2)
    left.line_chart(ramp, x=TIME, y=POWER, height=260)
    right.line_chart(ramp, x=TIME, y=TEMPS, height=260)
    st.caption("O balanço aproxima a potência elétrica absorvida como calor gerado. O calor removido depende da diferença de temperatura e da resistência térmica.")
    with st.expander("Resultados no fim de cada nível"):
        st.table([{field: number(row[field], digits) for field, digits in (
            ("Carga solicitada (%)", 0), ("CPU solicitada (%)", 1), ("GPU solicitada (%)", 1),
            ("CPU (A)", 1), ("GPU (A)", 1), ("CPU (GHz)", 2), ("GPU (GHz)", 2),
            (POWER, 1), ("CPU (°C)", 1), ("GPU (°C)", 1),
        )} for row in ramp[44::45]])

elif step == STEPS[2]:
    st.header("Mesma carga, três condições de refrigeração")
    runs = {name: simulate(activity, [(load, TEST_SECONDS)], name, start) for name in COOLING}
    summaries = {name: summarize(rows) for name, rows in runs.items()}
    selected = st.selectbox("Componente em destaque", ("CPU", "GPU"), index=int(focus == "GPU"))
    limit = THERMAL_LIMITS[int(selected == "GPU")]
    temp_key = f"{selected} (°C)"
    clock_key = f"{selected} (GHz)"
    series = [{TIME: row[TIME], temp_key: row[temp_key], clock_key: row[clock_key],
               "Refrigeração": name} for name, rows in runs.items() for row in rows]
    temperatures = [{TIME: row[TIME], temp_key: limit, "Refrigeração": "Limiar térmico"}
                    for row in runs["Adequada"]]
    left, right = st.columns(2)
    left.line_chart(series + temperatures, x=TIME, y=temp_key, color="Refrigeração", height=270)
    right.scatter_chart(series, x=temp_key, y=clock_key, color="Refrigeração", height=270)
    adequate, insufficient = summaries["Adequada"], summaries["Insuficiente"]
    first = insufficient["Primeira limitação (s)"]
    if first is not None:
        st.warning(f"Com refrigeração insuficiente, a limitação começou aos {first} s. "
                   f"O desempenho médio passou de {number(adequate[PERFORMANCE])}% para "
                   f"{number(insufficient[PERFORMANCE])}% em relação ao máximo de referência.")
    else:
        st.info("Nesta carga, os chips ficaram abaixo do limiar. Para observar a limitação, teste computação intensiva ou renderização a 100%.")
    comparison(summaries, ((temp_key.replace(selected, f"Pico {selected}", 1), 1), (clock_key, 2),
                           (POWER, 1), (PERFORMANCE, 1), ("Primeira limitação (s)", 0)))
    if first is not None:
        hot_run = runs["Insuficiente"]
        before, after = hot_run[0], hot_run[-1]
        st.caption(
            f"Sob a mesma demanda, do início ao fim do ensaio insuficiente, "
            f"a potência foi de {number(before[POWER])} a {number(after[POWER])} W "
            f"e o desempenho de {number(before[PERFORMANCE])}% a {number(after[PERFORMANCE])}%. "
            "A proteção térmica reduziu o clock e, com ele, o trabalho entregue e o calor gerado."
        )
    st.caption("Potência, clock e desempenho são médias de 180 s. Os três ensaios começam nas mesmas temperaturas da referência.")

else:
    st.header("Quanto trabalho útil se obtém por watt?")
    left, right = st.columns(2)
    reduction = left.slider("Redução da tensão da CPU (mV)", 0, 250, 70, step=10,
                            help="Experimente 180 mV em computação intensiva a 100% para observar falhas no modelo.")
    cooling = right.selectbox("Refrigeração nos dois testes", COOLING.keys())
    with st.expander("Controles adicionais da CPU"):
        clock = st.slider("Frequência alvo relativa (%)", 60, 100, 100, step=5)
        cap = st.slider("Limite de potência elétrica da CPU (W)", 30, 95, 95, step=5)
    runs = {
        name: simulate(activity, [(load, TEST_SECONDS)], cooling, start,
                       offset_mv=-offset, clock_ratio=clock / 100, cap_w=cap)
        for name, offset in (("Original", 0), ("Tensão reduzida", reduction))
    }
    summaries = {name: summarize(rows) for name, rows in runs.items()}
    original, adjusted = summaries.values()
    if adjusted["Travou"]:
        st.error(f"Travamento simulado. O modelo acumulou {adjusted['Erros simulados']} eventos de erro. "
                 "O tempo sem trabalho útil entra na média.")
    elif adjusted["Erros simulados"]:
        st.warning(f"A tensão selecionada gerou {adjusted['Erros simulados']} eventos de erro neste teste.")
    elif adjusted["Desempenho por W"] > original["Desempenho por W"]:
        gain = 100 * (adjusted["Desempenho por W"] / original["Desempenho por W"] - 1)
        st.success(f"Neste ensaio, o desempenho por watt aumentou {number(gain)}%.")
    else:
        st.info("Nesta configuração, a redução de tensão não elevou a eficiência média.")
    comparison(summaries, (("CPU (V)", 3), (POWER, 1), ("Pico CPU (°C)", 1),
                           ("CPU (GHz)", 2), (PERFORMANCE, 1), ("Desempenho por W", 3)))
    points = [{"Cenário": name, POWER: row[POWER], PERFORMANCE: row[PERFORMANCE]}
              for name, rows in runs.items() for row in rows]
    st.scatter_chart(points, x=POWER, y=PERFORMANCE, color="Cenário", height=240)
    st.caption("Mesma carga, refrigeração, clock alvo e limite de potência. Eficiência é o desempenho relativo médio dividido pela potência total média.")

with st.expander("Como o modelo calcula os resultados"):
    st.markdown(
        "**Elétrica.** A potência dinâmica segue α × C × V² × f. O modelo soma uma "
        "parcela fixa por chip e calcula a corrente por I = P ÷ V.\n\n"
        "**Térmica.** A condução pela interface e a convecção para o ar entram como "
        "resistências em série. A temperatura varia gradualmente a cada segundo simulado. "
        "Ao cruzar o limiar, o clock efetivo cai e a potência é recalculada.\n\n"
        "**Limites.** A margem de tensão, o índice de desempenho e os eventos de erro "
        "são parâmetros educativos. As saídas são resultados calculados para o computador virtual."
    )
    st.caption("Referência: trabalho acadêmico da UEMG, seções 1.3, 2.1.1 a 2.3.1 e 4. "
               "O documento identifica o simulador como EnergySim.")
