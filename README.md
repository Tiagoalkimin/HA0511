# EnergyLens

Demonstração de eficiência energética de computadores. Um único cenário mostra o consumo normal, o desperdício e o resultado de uma otimização.

## Executar

Na pasta que contém app.py, com Python 3.10 ou superior:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para publicar no Streamlit Community Cloud, coloque o conteúdo desta pasta no repositório e selecione app.py como arquivo principal.

## Apresentar em cerca de 2 minutos

1. **0 a 30 segundos.** Mostre o computador usando navegador e documentos. Aponte a potência inicial.
2. **30 a 70 segundos.** Clique em **Simular desperdício**. Mostre a potência, a temperatura e o alerta. Explique que processos dispensáveis em segundo plano podem aumentar o consumo.
3. **70 a 120 segundos.** Clique em **Aplicar otimização**. Compare o pico de desperdício com o resultado otimizado e destaque a economia mensal estimada. Mostre no gráfico que a potência retorna ao patamar inicial.

Os dois cliques calculam os resultados imediatamente. Use **Reiniciar demonstração** para voltar à primeira etapa.

## Modelo

As curvas de potência de CPU e GPU, o cálculo de energia, o modelo térmico exponencial e a margem de 15% acima do máximo esperado para a tarefa vêm da versão anterior. O cenário adiciona 90 W ilustrativos e a otimização remove essa parcela, mantendo a carga útil. Cada etapa avança três minutos no modelo térmico. O custo e a energia mensal projetam 8 horas de uso por dia durante 30 dias a R$ 0,90 por kWh. Os valores são simulados.
