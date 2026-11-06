# EnergyLens

Laboratório virtual para comparar potência, aquecimento e desempenho de um mesmo computador. A tela abre diretamente nos ensaios. Os parâmetros são ilustrativos.

## Execução

Na pasta que contém `app.py`:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para o Streamlit Community Cloud, selecione `app.py` como arquivo principal. A versão anterior fica disponível localmente por `python -m streamlit run app_original.py`.

## Roteiro para a banca

1. **Carga.** Use Processamento de IA e compare a referência de 25% com 100%. Mostre primeiro a potência. Selecione a temperatura da CPU no gráfico para mostrar o aquecimento gradual.
2. **Refrigeração.** Mantenha a atividade e a carga. Compare a condição adequada com a insuficiente. Mostre o cruzamento do limiar e depois selecione frequência ou desempenho no gráfico. A comparação conserva as temperaturas iniciais e a duração.
3. **Tensão.** Use refrigeração adequada e teste 70 mV de redução. Mostre a queda de potência com desempenho equivalente no cenário padrão. Depois teste 180 mV. O gráfico de desempenho mostra a interrupção do trabalho no travamento simulado.

Os detalhes de tensão, corrente, frequência, potência por componente, energia e eficiência ficam em **Dados dos dois cenários**. O painel **Configuração do ensaio** permite alterar duração, frequência alvo e teto elétrico da CPU.

## Método e interpretação

* O computador intermediário reaproveita os perfis de CPU, GPU e componentes auxiliares do projeto anterior. A integração da energia e a resposta térmica exponencial também reaproveitam funções existentes.
* O modelo de ensaio calcula potência dinâmica proporcional à atividade, ao quadrado da tensão e à frequência. A corrente estimada de cada chip segue I = P/V. Os valores de tensão são internos aos circuitos modelados.
* A refrigeração altera as resistências de condução e convecção. A CPU e a GPU têm temperaturas independentes. Acima dos limiares ilustrativos de 84 °C e 83 °C, respectivamente, a frequência efetiva cai e a potência é recalculada.
* A redução de tensão atua na CPU. Se ela ficar abaixo da margem de estabilidade do modelo, o trabalho útil é afetado e a exposição pode causar travamento. O gráfico inclui a interrupção do processamento.
* O índice de desempenho é relativo ao máximo teórico da mesma atividade. Desempenho por watt é o índice médio dividido pela potência total média. Os resultados servem para comparação virtual. Os parâmetros ainda exigem calibração para representar um equipamento específico.

## Conferência com a metodologia escrita

Antes da entrega, confira se o nome e o link do simulador no texto correspondem aos da versão apresentada. Use **índice de desempenho por watt** para descrever a métrica desta versão. Atualize resultados ou figuras anteriores caso tenham sido gerados com o modelo antigo.
