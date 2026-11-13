"""Demonstração de palco do EnergySim. Cálculos preservados em core/demo.py."""
import html
import streamlit as st
from core.demo import QuickDemo
from models.computer import hardware_details
from core.energy import cost_projection


def br(value, digits=1):
    return f"{value:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def render_demo():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {color-scheme:light;}
    .stApp {background:#f7f6f2;color:#243b38;font-family:'DM Sans',sans-serif;}
    .block-container {max-width:1160px;padding-top:2.25rem;padding-bottom:2rem;}
    [data-testid="stHeader"] {background:transparent;}
    [data-testid="stVerticalBlock"] {gap:.8rem;}
    h1,h2,h3,p {font-family:'DM Sans',sans-serif;}
    .el-hardware {background:#fff;border:1px solid #d4dfd6;border-radius:16px;padding:18px 20px;margin:12px 0;}
    .el-hardware h3 {font-size:1rem;margin:0 0 14px;}
    .el-specs {display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;}
    .el-spec small {display:block;color:#687a72;font-size:.78rem;}
    .el-spec b {display:block;font-size:.88rem;color:#253f37;}
    .el-hardware p {font-size:.76rem;color:#72837a;margin:14px 0 0;}
    .el-kicker {font-size:.79rem;font-weight:800;letter-spacing:.12em;color:#38786a;text-transform:uppercase;margin-bottom:12px;}
    .el-hero {display:flex;align-items:center;justify-content:space-between;gap:20px;padding-bottom:8px;}
    .el-title {font-family:'Manrope',sans-serif;font-size:clamp(2.1rem,4vw,3.35rem);font-weight:800;line-height:1.12;letter-spacing:-.055em;color:#203d37;margin:0 0 10px;}
    .el-sub {font-size:1.07rem;color:#677a73;line-height:1.55;max-width:630px;margin:0 0 14px;}
    .el-brand {font-family:'Manrope',sans-serif;font-size:1.1rem;font-weight:800;color:#2b5c51;border:1px solid #d4dfd6;border-radius:50px;padding:11px 18px;white-space:nowrap;background:#fff;}
    .el-brand span {color:#d4a55c;}
    .el-steps {display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin:14px 0 8px;}
    .el-step {background:#fff;border:1px solid #e5e8e0;border-radius:15px;padding:14px 16px;color:#88958e;display:flex;gap:11px;align-items:center;}
    .el-step .el-num {font-weight:800;font-size:1rem;background:#f3f4f0;border-radius:50%;width:32px;height:32px;display:grid;place-items:center;flex-shrink:0;}
    .el-step b {font-size:.91rem;display:block;color:#536962;}
    .el-step small {font-size:.75rem;display:block;line-height:1.3;margin-top:2px;}
    .el-step.active {border-color:#8ebbaa;background:#edf6f0;box-shadow:0 4px 20px #255c3e0d;}
    .el-step.active .el-num {background:#2d6e59;color:#fff;}
    .el-step.active b {color:#275947;}
    .el-context {font-size:.87rem;color:#687c74;margin:13px 0 5px;}
    .el-context strong {color:#314e44;}
    .el-kpis {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:12px 0 16px;}
    .el-kpi {background:#fff;border:1px solid #e6e9e1;border-radius:16px;padding:20px 19px;min-height:124px;box-shadow:0 4px 20px #1a3b2606;}
    .el-kpi-label {font-size:.85rem;font-weight:600;color:#687a72;}
    .el-kpi-val {font-family:'Manrope',sans-serif;font-weight:800;font-size:clamp(1.4rem,2.4vw,1.95rem);letter-spacing:-.05em;color:#253f37;margin-top:12px;line-height:1.1;}
    .el-kpi-unit {font-size:.78rem;font-weight:500;color:#8b9a92;margin-top:6px;}
    .el-story {display:flex;gap:14px;align-items:flex-start;padding:20px 22px;border-radius:16px;border:1px solid #dce5dc;background:#eaf2e9;margin:8px 0 16px;}
    .el-story.warning {background:#fff2e9;border-color:#ecd6c4;}
    .el-story.good {background:#e7f3ec;border-color:#bbd8c5;}
    .el-story-icon {font-size:1.6rem;line-height:1.1;}
    .el-story h3 {font-size:1.13rem;margin:0 0 5px;font-weight:800;color:#29483d;}
    .el-story p {font-size:.93rem;line-height:1.55;color:#526b60;margin:0;}
    .el-story.warning h3 {color:#86502f;}
    .el-panel {background:#fff;border:1px solid #e5e8e0;border-radius:18px;padding:23px 25px;margin:4px 0 12px;}
    .el-panel h3 {font-size:1.08rem;font-weight:800;color:#2c4b3e;margin:0 0 17px;}
    .el-compare-row {display:flex;justify-content:space-between;gap:10px;font-size:.89rem;color:#556960;margin:14px 0 8px;}
    .el-compare-row b {color:#263f35;}
    .el-track {width:100%;height:17px;background:#f0f1ed;border-radius:12px;overflow:hidden;}
    .el-fill {height:100%;border-radius:12px;}
    .el-before {background:#df9a71;}
    .el-after {background:#5b9d7c;}
    .el-fine {color:#72837a;font-size:.82rem;margin-top:17px;line-height:1.5;}
    .el-outcome {background:#285a47;border-radius:18px;padding:24px;color:white;margin:4px 0 12px;}
    .el-outcome .el-t {font-size:.83rem;opacity:.85;}
    .el-outcome .el-v {font-family:'Manrope',sans-serif;font-weight:800;font-size:2.55rem;letter-spacing:-.06em;line-height:1.12;margin:6px 0 17px;}
    .el-outcome .el-v.small {font-size:2rem;}
    .el-outcome .el-line {height:1px;background:#ffffff30;margin-bottom:16px;}
    .el-outcome .el-foot {font-size:.83rem;color:#d6ebdf;}
    .stButton button {min-height:49px;border-radius:12px;font-weight:700;font-family:'DM Sans',sans-serif;}
    .stButton button[kind="primary"] {background:#2e7058;border-color:#2e7058;color:#fff;}
    .stButton button[kind="secondary"] {border-color:#d8dfd7;background:#fff;color:#375448;}
    .stButton button:disabled {opacity:.44;}
    div[data-testid="stExpander"] {background:#fff;border:1px solid #e3e7df;border-radius:14px;}
    .el-disclaimer {font-size:.79rem;color:#788880;line-height:1.55;margin-top:7px;}
    @media(max-width:760px) {.el-kpis{grid-template-columns:repeat(2,1fr)}.el-steps{grid-template-columns:1fr}.el-brand{display:none}.block-container{padding-top:1.2rem}.el-title{font-size:2rem}}
    </style>""", unsafe_allow_html=True)

    if "quick_demo" not in st.session_state:
        st.session_state.quick_demo = QuickDemo()
    demo = st.session_state.quick_demo
    snap = demo.snapshot()
    power = snap["power"]["total_w"]
    month = cost_projection(power, demo.tariff)["30d"]
    stage = demo.stage
    index = {"normal": 0, "waste": 1, "optimized": 2}[stage]
    st.markdown('''<div class="el-hero"><div><div class="el-kicker">Tecnologia para consumir com consciência</div>
       <div class="el-title">Energia que você não vê.<br>Economia que você sente.</div>
       <p class="el-sub">Descubra como atividades em segundo plano podem aumentar o consumo do computador, mesmo quando a sua tarefa não muda.</p></div>
       <div class="el-brand"><span>✦</span> EnergySim</div></div>''', unsafe_allow_html=True)
    steps = [("Observe", "Como o computador está agora"), ("Identifique", "O que está consumindo a mais"), ("Compare", "O resultado da otimização")]
    segments = []
    for i, (title, desc) in enumerate(steps):
        segments.append(f'<div class="el-step {"active" if i == index else ""}"><span class="el-num">{i+1}</span><div><b>{title}</b><small>{desc}</small></div></div>')
    st.markdown('<div class="el-steps">'+''.join(segments)+'</div>', unsafe_allow_html=True)
    st.markdown('<div class="el-context"><strong>Nosso cenário:</strong> computador intermediário, navegador e documentos abertos. A tarefa permanece igual nos três momentos.</div>', unsafe_allow_html=True)
    specs = hardware_details(demo.sim.computer)
    cards = ''.join(
        f'<div class="el-spec"><small>{html.escape(label)}</small><b>{html.escape(value)}</b></div>'
        for label, value in specs
    )
    st.markdown('<div class="el-hardware"><h3>Computador desta simulação</h3><div class="el-specs">' + cards + '</div><p>Configuração de referência. Não é uma detecção do seu computador. Turbo é um limite eventual; consumo, temperatura e clock são estimativas didáticas.</p></div>', unsafe_allow_html=True)
    kpis = [
        ("Consumo neste momento", f"{br(power, 1)} W", "Potência elétrica estimada"),
        ("Temperatura", f"{br(snap['temp'], 1)} °C", "Valor estimado pelo modelo"),
        ("Uso do processador", f"{br(snap['cpu_util'], 0)}%", f"Placa gráfica: {br(snap['gpu_util'], 0)}%"),
        ("Custo em 30 dias", f"R$ {br(month['custo'], 2)}", "8 horas por dia, tarifa simulada"),
    ]
    st.markdown('<div class="el-kpis">'+''.join(f'<div class="el-kpi"><div class="el-kpi-label">{html.escape(a)}</div><div class="el-kpi-val">{html.escape(b)}</div><div class="el-kpi-unit">{html.escape(c)}</div></div>' for a,b,c in kpis)+'</div>', unsafe_allow_html=True)

    if stage == "normal":
        story = ("🌿", "Tudo dentro do esperado", "O computador está executando tarefas simples. Agora vamos mostrar o que acontece quando processos extras consomem energia sem contribuir para o trabalho.", "")
    elif stage == "waste":
        story = ("⚠️", "Algo está gastando energia sem necessidade", f"A tarefa continua a mesma, mas há {br(snap['power']['waste_w'], 0)} W extras no cenário simulado. Pense em abas com vídeos, programas esquecidos, atualizações ou sincronizações desnecessárias. O EnergySim sinaliza essa diferença para investigação.", "warning")
    else:
        story = ("✓", "Mesmo trabalho, menor consumo", "A intervenção simulada eliminou a parcela adicional de energia. A carga útil de CPU e GPU foi preservada. Veja a comparação e o efeito projetado no custo.", "good")
    ico, title, desc, kind = story
    st.markdown(f'<div class="el-story {kind}"><div class="el-story-icon">{ico}</div><div><h3>{html.escape(title)}</h3><p>{html.escape(desc)}</p></div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 2, 1])
    c1.button("1. Mostrar consumo extra", type="primary" if stage == "normal" else "secondary", disabled=stage != "normal", on_click=demo.inject_waste, use_container_width=True)
    c2.button("2. Simular otimização", type="primary" if stage == "waste" else "secondary", disabled=stage != "waste", on_click=demo.optimize, use_container_width=True)
    def reset():
        st.session_state.quick_demo = QuickDemo(demo.tariff)
    c3.button("Recomeçar", on_click=reset, use_container_width=True)

    result = demo.comparison()
    if result:
        left, right = st.columns([3, 2], gap="medium")
        before_w, after_w = result["before_w"], result["after_w"]
        ratio = after_w / before_w * 100 if before_w else 0
        with left:
            st.markdown(f'''<div class="el-panel"><h3>O que mudou na prática?</h3>
            <div class="el-compare-row"><span>Com consumo desnecessário</span><b>{br(before_w)} W</b></div>
            <div class="el-track"><div class="el-fill el-before" style="width:100%"></div></div>
            <div class="el-compare-row"><span>Após a otimização simulada</span><b>{br(after_w)} W</b></div>
            <div class="el-track"><div class="el-fill el-after" style="width:{ratio:.2f}%"></div></div>
            <div class="el-fine">Temperatura estimada: {br(result['before_temp'])} °C → {br(result['after_temp'])} °C<br>
            Custo em 30 dias: R$ {br(result['before_month']['custo'],2)} → R$ {br(result['after_month']['custo'],2)}</div></div>''', unsafe_allow_html=True)
        with right:
            st.markdown(f'''<div class="el-outcome"><div class="el-t">Redução da potência no cenário</div><div class="el-v">{br(result['reduction_pct'])}%</div>
            <div class="el-line"></div><div class="el-t">Economia projetada em 30 dias</div><div class="el-v small">R$ {br(result['saved_brl'],2)}</div>
            <div class="el-foot">{br(result['saved_kwh'],2)} kWh a menos no mesmo período de uso</div></div>''', unsafe_allow_html=True)
    else:
        normal_min = snap["anomaly"]["esperado_min"]
        normal_max = snap["anomaly"]["esperado_max"]
        st.markdown(f'<div class="el-disclaimer">Faixa de consumo de referência da tarefa: {br(normal_min)} a {br(normal_max)} W. O modelo sinaliza uma anomalia acima de {br(normal_max * 1.15)} W.</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="el-disclaimer">Demonstração educativa, sem leitura de sensores nem alteração de processos reais. Projeção: 8 h por dia, durante 30 dias, com tarifa ilustrativa de R$ {br(demo.tariff,2)} por kWh e consumo constante. Cada etapa térmica representa três minutos simulados. Os 90 W adicionais são uma hipótese de teste, não uma medida de aplicativos específicos.</div>', unsafe_allow_html=True)
    with st.expander("Entenda as premissas e explore o simulador completo"):
        st.write("Esta é uma simulação controlada. A intervenção aplica a ação 'verificar processos' do modelo, sem encerrar nenhum programa real. O alerta compara a potência total com uma faixa esperada da tarefa, acrescida de 15% de tolerância. A economia compara a mesma carga útil e as mesmas 240 horas mensais antes e depois.")
        st.write("Atualizações, sincronizações e backups nem sempre são desperdício: o excesso precisa ser confirmado em uma implementação com sensores e processos reais. A temperatura varia ao longo do tempo e não cai imediatamente em hardware físico.")
        tariff = st.number_input("Tarifa utilizada no exemplo (R$/kWh)", min_value=0.10, max_value=3.0, value=demo.tariff, step=0.05, key="demo_tariff")
        if tariff != demo.tariff:
            demo.tariff = tariff
            demo.sim.tarifa_kwh = tariff
            st.rerun()
        st.write("O modo completo inclui seleção de computadores e atividades, relatórios, testes de estresse e experimentos.")
        if st.button("Explorar o modo completo"):
            st.session_state.screen = "intro_problema"
            st.rerun()
