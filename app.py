"""Interface de apresentação dos ensaios EnergyLens."""

import pandas as pd
import streamlit as st

from core.bench import ACTIVITIES, AMBIENTE_C, AUXILIARY_W, COOLING, THERMAL_LIMITS, simulate, summarize

st.set_page_config(page_title="EnergyLens", layout="wide")

TIME = "Tempo (s)"
POWER = "Potência total (W)"
PERFORMANCE = "Desempenho (%)"
ENERGY = "Energia (Wh)"
EFFICIENCY = "Desempenho por W"
EXPERIMENTS = {
    "Carga": "Como a demanda altera o consumo e o aquecimento?",
    "Refrigeração": "Quando o calor limita o desempenho?",
    "Tensão": "É possível consumir menos mantendo o desempenho?",
}


def number(value, digits=1):
    return f"{value:.{digits}f}".replace(".", ",")


def describe_run(rows, summary, chip, name):
    last = rows[-1]
    return {
        "Cenário": name,
        "Potência média (W)": round(summary[POWER], 1),
        "Energia (Wh)": round(summary[ENERGY], 2),
        "Pico CPU (°C)": round(summary["Pico CPU (°C)"], 1),
        "Pico GPU (°C)": round(summary["Pico GPU (°C)"], 1),
        "Tensão final da CPU (V)": round(last["CPU (V)"], 3),
        "Corrente final da CPU (A)": round(last["CPU (A)"], 2),
        f"Clock médio da {chip} (GHz)": round(summary[f"{chip} (GHz)"], 2),
        "Desempenho médio (%)": round(summary[PERFORMANCE], 1),
        "Eficiência (p.p./W)": round(summary[EFFICIENCY], 3),
        "Início da limitação (s)": summary["Primeira limitação (s)"],
        "Tempo em limitação (s)": summary["Tempo em limitação (s)"],
        "Erros simulados": summary["Erros simulados"],
        "Travamento (s)": summary["Travamento (s)"],
    }


st.title("EnergyLens")
st.caption("Laboratório virtual de consumo, temperatura e desempenho")
experiment = st.radio("Ensaio", EXPERIMENTS, horizontal=True)
st.subheader(EXPERIMENTS[experiment])

left, right = st.columns(2)
activity = left.selectbox("Atividade", tuple(ACTIVITIES), index=2)
load = right.selectbox("Demanda do cenário testado", (25, 50, 75, 100), index=3,
                       format_func=lambda value: f"{value}%")
chip = "GPU" if activity == "Renderização gráfica" else "CPU"
temp_key = f"{chip} (°C)"
clock_key = f"{chip} (GHz)"

cooling = "Adequada"
tested_cooling = "Adequada"
offset = 0
if experiment == "Refrigeração":
    tested_cooling = st.selectbox("Refrigeração testada", ("Insuficiente", "Limitada"))
elif experiment == "Tensão":
    offset = st.slider("Redução da tensão da CPU (mV)", 0, 220, 70, step=10)
    tested_cooling = cooling = st.selectbox("Refrigeração nos dois cenários", COOLING)

with st.expander("Configuração do ensaio"):
    duration = st.select_slider("Duração simulada (min)", (2, 3, 5, 8, 10), value=5)
    clock = st.slider("Frequência alvo da CPU (%)", 60, 100, 100, step=5)
    cap = st.slider("Limite elétrico da CPU (W)", 30, 95, 95, step=5)
    st.caption("A frequência alvo e o limite elétrico valem para os dois cenários. O limite em watts é um teto do modelo.")

# Os dois cenários partem da mesma temperatura. Só a variável do ensaio muda.
base_load = 25 if experiment == "Carga" else load
base_label, test_label = {
    "Carga": ("Referência · 25%", f"Teste · {load}%"),
    "Refrigeração": ("Refrigeração adequada", f"Refrigeração {tested_cooling.lower()}"),
    "Tensão": ("Tensão original", f"Tensão reduzida · {offset} mV"),
}[experiment]
settings = {"clock_ratio": clock / 100, "cap_w": cap}
base_rows = simulate(activity, [(base_load, duration * 60)], cooling, **settings)
test_rows = simulate(activity, [(load, duration * 60)], tested_cooling, offset_mv=-offset, **settings)
base, test = summarize(base_rows), summarize(test_rows)
st.caption(f"Mesmo computador virtual · {duration} min simulados · Temperatura inicial de {AMBIENTE_C:g} °C")

peak = f"Pico {chip} (°C)"
columns = st.columns(3)
for column, label, key, unit, difference_unit in zip(
    columns,
    ("Potência média", f"Pico da {chip}", "Desempenho médio"),
    (POWER, peak, PERFORMANCE),
    ("W", "°C", "%"),
    ("W", "°C", "p.p."),
):
    difference = test[key] - base[key]
    column.metric(label, f"{number(test[key])} {unit}",
                  f"{difference:+.1f}".replace(".", ",") + f" {difference_unit}",
                  delta_color="off", help="Diferença em relação ao cenário de referência.")

if experiment == "Carga":
    fields = (POWER, temp_key, PERFORMANCE, "Energia (Wh)")
elif experiment == "Refrigeração":
    fields = (temp_key, clock_key, PERFORMANCE, POWER)
else:
    fields = (POWER, PERFORMANCE, "CPU (°C)", "CPU (V)")
field = st.radio("Métrica do gráfico", fields, horizontal=True, key=f"chart_{experiment}")
series = pd.DataFrame({
    TIME: [row[TIME] for row in base_rows],
    base_label: [row[field] for row in base_rows],
    test_label: [row[field] for row in test_rows],
})
colors = ["#63778A", "#08665C"]
if field in ("CPU (°C)", "GPU (°C)") and experiment == "Refrigeração":
    series["Limiar térmico"] = THERMAL_LIMITS[int(field.startswith("GPU"))]
    colors.append("#A65B1B")
st.line_chart(series, x=TIME, y=[column for column in series if column != TIME],
              y_label=field, color=colors, height=300)

if test["Travou"]:
    st.error(f"O processamento travou aos {test['Travamento (s)']} s simulados. A queda de potência acompanha a interrupção do trabalho.")
elif test["Erros simulados"]:
    st.warning(f"A tensão testada gerou {test['Erros simulados']} eventos de erro no modelo.")
elif experiment == "Refrigeração":
    onset = test["Primeira limitação (s)"]
    if onset is None:
        st.info("Nesta configuração, nenhum componente entrou em limitação térmica no cenário testado.")
    else:
        st.warning(f"A limitação térmica começou aos {onset} s e ocorreu por {test['Tempo em limitação (s)']} s no cenário testado.")
elif experiment == "Tensão":
    efficiency_change = 100 * (test[EFFICIENCY] / base[EFFICIENCY] - 1)
    st.caption(f"Variação de eficiência: {number(efficiency_change)}% em desempenho por watt.")
else:
    st.caption("A potência muda com a carga solicitada. A temperatura evolui à medida que os componentes acumulam e dissipam calor.")

with st.expander("Dados dos dois cenários"):
    summary_table = pd.DataFrame([
        describe_run(base_rows, base, chip, base_label),
        describe_run(test_rows, test, chip, test_label),
    ]).set_index("Cenário").T
    st.table(summary_table.astype("string").fillna("Não ocorreu"))
    st.caption("O desempenho é um índice relativo à mesma atividade. A eficiência divide o índice médio pela potência média.")
    st.table(pd.DataFrame({
        "Componente": ["CPU", "GPU", *AUXILIARY_W],
        "Potência no fim do teste (W)": [
            round(test_rows[-1]["CPU (W)"], 1), round(test_rows[-1]["GPU (W)"], 1), *AUXILIARY_W.values()
        ],
    }))
st.caption("Resultados calculados com parâmetros ilustrativos. Os indicadores representam um computador virtual.")
