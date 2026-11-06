# EnergyLens · Laboratório virtual

Simulação em quatro etapas para o trabalho **Consumo Elétrico por um Computador sobre Condições de Funcionamento Elevadas e Irregulares**, de Pedro Henrique Silva Teixeira e Tiago Monteiro Alkimin, UEMG, 2026. O trabalho escrito chama o simulador de EnergySim. A aplicação mantém o nome EnergyLens.

## Executar

Abra o terminal na pasta que contém `app.py`. Use Python 3.10 ou superior.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No Streamlit Community Cloud, selecione `app.py` como arquivo principal. O tema está em `.streamlit/config.toml`.

## Roteiro de cerca de dois minutos

1. **Referência, 20 s.** Mantenha Computação intensiva. A referência roda a 25% da demanda. Mostre potência, temperatura dos chips e energia acumulada. Os valores elétricos e a decomposição por componente ficam no painel expansível.
2. **Demanda, 30 s.** Mantenha 100% como carga final. A rampa percorre 25%, 50%, 75% e 100% durante 45 s simulados em cada nível. Veja potência e temperatura. Se houver tempo, troque para Renderização gráfica e observe a GPU.
3. **Refrigeração, 35 s.** Use Computação intensiva e 100%. Compare os três perfis com carga, duração e temperatura inicial iguais. Leia o primeiro segundo de limitação e a queda de clock e desempenho.
4. **Eficiência, 35 s.** Com a mesma atividade e carga, deixe a refrigeração adequada. Compare o padrão e a redução de 70 mV. Aumente a redução para 180 mV para demonstrar instabilidade e travamento nas condições padrão. Esses valores pertencem ao modelo.

## Relação com o trabalho escrito

| Seção | Implementação |
| --- | --- |
| 1.3 e 4 | Comparações controladas de carga, arrefecimento, tensão e frequência, com séries temporais reproduzíveis. |
| 2.1.1 e 2.1.2 | Potência dinâmica por αCV²f, parcela estática fixa e corrente por I = P/V. Os perfis de tarefa distribuem a demanda entre os chips. |
| 2.1.3 e 2.2.1 | Resistências efetivas de condução e convecção em série, dinâmica térmica e limitação de clock por temperatura. |
| 2.3.1 | Comparação de tensão, potência, temperatura, clock, desempenho e desempenho por watt. Redução excessiva de tensão acumula falhas simuladas. |

## Premissas e interpretação

* A potência dinâmica usa a demanda de cada chip como proxy para α. A capacitância efetiva é calibrada com os valores de repouso e pico da versão anterior. A tensão estimada cresce com o clock. Para o ensaio de undervolting, o deslocamento de tensão atua somente na CPU.
* CPU e GPU têm estados térmicos independentes. A condução agrega o efeito de material, espessura e área de contato, representado por uma resistência efetiva análoga a d/(kA). A convecção agrega a área do dissipador e o fluxo de ar, com resistência análoga a 1/(hA). Os perfis de arrefecimento alteram essas resistências, conservando os limites de 84 °C para CPU e 83 °C para GPU.
* O balanço aproxima a potência elétrica como calor gerado. A temperatura de equilíbrio de cada chip é o ar efetivo mais a potência do chip vezes a resistência térmica. A temperatura evolui exponencialmente com constante de tempo igual à resistência térmica vezes a capacidade térmica. A carga auxiliar aquece o ar efetivo por um acoplamento fixo simplificado.
* No passo seguinte ao cruzamento do limiar, o clock efetivo diminui em função do excesso térmico. Isso altera a potência dinâmica e o trabalho útil. O teto de potência elétrica atua sobre a frequência da CPU a tensão fixa naquele passo. O teto é um parâmetro operacional, distinto da especificação térmica TDP.
* A margem de tensão depende da frequência. A exposição a uma tensão abaixo da margem reduz o trabalho útil, acumula erros modelados e eventualmente trava a execução. Após o travamento, o trabalho útil fica em zero e a potência dos chips cai à parcela de repouso.
* O desempenho é um índice relativo ao máximo teórico da mesma tarefa, calculado pela demanda e pela frequência efetiva de CPU e GPU. Compare o índice entre ensaios da mesma atividade. A eficiência é a média do índice dividida pela média da potência total no mesmo intervalo. Os gráficos mostram resultados calculados, sem FPS ou telemetria física.
* Placa mãe e VRM permanecem agrupados. RAM, NVMe e ventoinhas têm parcelas fixas. Os parâmetros são ilustrativos e servem a uma comparação virtual. A simulação carece de calibração experimental para prever um equipamento específico.
