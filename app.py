import streamlit as st

from core.demo import DAYS_PER_MONTH, HOURS_PER_DAY, TARIFF, THERMAL_INTERVAL_S, QuickDemo

st.set_page_config(page_title="EnergyLens", page_icon="⚡", layout="wide")
st.markdown(
    """
    <style>
    .block-container {max-width: 1050px; padding-top: 3rem;}
    [data-testid="stMetricValue"] {font-size: clamp(1.3rem, 3vw, 2.35rem);}
    .stage {color:#58dec1; font-weight:700; letter-spacing:.08em; font-size:.85rem;}
    .power-row {margin:.65rem 0;}
    .power-label {display:flex; justify-content:space-between; gap:.5rem; margin-bottom:.3rem;}
    .power-track {height:.55rem; background:#27354a; border-radius:1rem;}
    .power-fill {height:100%; border-radius:1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def br(value, places=1):
    return f"{value:.{places}f}".replace(".", ",")


def reset():
    st.session_state.demo = QuickDemo()


if "demo" not in st.session_state:
    reset()

demo = st.session_state.demo
reading = demo.optimized or demo.waste or demo.initial
stage = 3 if demo.optimized else 2 if demo.waste else 1
stage_title = ("Consumo normal", "Desperdício", "Resultado")[stage - 1]

st.title("⚡ EnergyLens")
st.markdown(f'<div class="stage">ETAPA {stage} DE 3 · {stage_title.upper()}</div>', unsafe_allow_html=True)
st.caption("🖥️ Computador em uso · Navegador e documentos · Simulação ilustrativa")

metric_specs = (
    ("Potência", "power_w", "W", 1),
    ("Temperatura estimada", "temperature_c", "°C", 1),
    ("Energia estimada por mês", "monthly_kwh", "kWh", 2),
    ("Custo estimado por mês", "monthly_cost", "R$", 2),
)

for column, (label, field, unit, places) in zip(st.columns(4), metric_specs):
    value = getattr(reading, field)
    formatted = f"R$ {br(value, places)}" if unit == "R$" else f"{br(value, places)} {unit}"
    delta = None
    if demo.optimized:
        saved = getattr(demo.waste, field) - value
        delta = f"R$ {br(saved, places)} a menos" if unit == "R$" else f"{br(saved, places)} {unit} a menos"
    column.metric(label, formatted, delta, border=True)

if stage == 1:
    st.info("Tarefas em segundo plano podem aumentar o consumo durante um uso simples.")
    st.button("Simular desperdício", type="primary", on_click=demo.inject_waste)
elif stage == 2:
    if demo.has_anomaly(reading):
        st.warning(f"Consumo acima do esperado para esta tarefa. Limite de alerta de {br(demo.alert_limit_w)} W.")
        st.write("**Recomendação.** Pausar processos dispensáveis em segundo plano, como downloads e sincronizações que podem esperar.")
        st.button("Aplicar otimização", type="primary", on_click=demo.optimize)
else:
    saved_pct = (demo.waste.power_w - reading.power_w) / demo.waste.power_w * 100
    st.success(f"Potência {br(saved_pct)}% menor que no pico de desperdício. A tarefa principal continua ativa.")
    st.subheader("Potência nas três etapas")
    states = (
        ("Inicial", demo.initial, "#92a9c4"),
        ("Com desperdício", demo.waste, "#f7ab67"),
        ("Otimizado", demo.optimized, "#58dec1"),
    )
    bars = []
    max_power = max(state.power_w for _, state, _ in states)
    for label, state, color in states:
        width = state.power_w / max_power * 100
        bars.append(
            f'<div class="power-row"><div class="power-label">'
            f'<span>{label}</span><strong>{br(state.power_w)} W</strong></div>'
            f'<div class="power-track" aria-hidden="true">'
            f'<div class="power-fill" style="width:{width:.2f}%;background:{color}"></div></div></div>'
        )
    st.markdown("".join(bars), unsafe_allow_html=True)
    st.button("Reiniciar demonstração", on_click=reset)

st.caption(
    f"Projeção mensal de {HOURS_PER_DAY} h por dia durante {DAYS_PER_MONTH} dias, "
    f"a R$ {br(TARIFF, 2)} por kWh. Cada etapa calcula {THERMAL_INTERVAL_S // 60} min "
    "de evolução térmica simulada, sem espera."
)
