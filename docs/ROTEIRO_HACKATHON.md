# EnergySim | Roteiro de apresentação para a banca

## Objetivo da apresentação

**Duração sugerida: 2 minutos de demonstração e até 1 minuto para perguntas.** Apresente o EnergySim como um protótipo de simulação, não como um monitor de sensores reais. O foco é mostrar que o consumo extra pode ser detectado e que o impacto de uma intervenção pode ser estimado.

## 00:00 a 00:20 | Apresentar uma situação do cotidiano

**Fala:**

> Imagine estar estudando, trabalhando em um documento ou navegando na internet. Tudo parece normal. Mas e se o computador estiver gastando muito mais energia do que precisa, mesmo sem você perceber? Essa é a questão que motivou o EnergySim.

**Na tela:** Abra a demonstração no estágio inicial. Aponte o título e depois o indicador *Consumo neste momento*. Não abra configurações nem o modo completo.

## 00:20 a 00:42 | Mostrar o consumo normal

**Fala:**

> Para mostrar a ideia, montamos uma simulação controlada. Aqui temos um computador intermediário executando uma tarefa simples: navegador e documentos. Os indicadores mostram potência, temperatura, uso do processador e estimativa de custo mensal. Vamos manter exatamente a mesma tarefa durante todo o teste.

**Na tela:** Aponte brevemente os quatro indicadores. Evite ler todos os números em voz alta.

## 00:42 a 01:05 | Revelar o problema

**Ação:** Clique em **1. Mostrar consumo extra**.

**Fala:**

> Agora adicionamos um consumo de 90 watts, representando processos desnecessários em segundo plano. Podem existir abas esquecidas, aplicativos ativos ou sincronizações que precisam ser investigadas. Percebam: a atividade principal continua igual, mas a potência aumentou. O EnergySim compara esse consumo com a referência esperada para a tarefa e destaca a anomalia.

**Na tela:** Aponte o indicador de potência e a mensagem de alerta. Ressalte que os 90 watts são uma hipótese ilustrativa e não uma medição dos aplicativos citados.

## 01:05 a 01:28 | Aplicar a intervenção

**Ação:** Clique em **2. Simular otimização**.

**Fala:**

> O próximo passo é avaliar a intervenção. Nosso modelo simula a remoção desse consumo extra, mantendo a mesma carga útil de CPU e GPU. A comparação aparece imediatamente, com a potência anterior e a posterior. A temperatura também é estimada ao longo de um intervalo simulado, não reduzida de forma instantânea em um equipamento real.

**Na tela:** Mostre as duas barras comparativas. Evite afirmar que o protótipo fechou programas de verdade.

## 01:28 a 01:50 | Traduzir o resultado

**Fala:**

> O principal resultado é que conseguimos traduzir uma diferença técnica em algo que qualquer pessoa entende. Neste exemplo, com oito horas por dia, trinta dias de uso e tarifa de noventa centavos por quilowatt hora, reduzir 90 watts representa 21,6 quilowatts hora, ou R$ 19,44 por mês. É uma projeção condicionada ao cenário, não uma promessa de economia real.

**Na tela:** Aponte o percentual, os kWh e o valor em reais, no painel verde.

## 01:50 a 02:00 | Encerramento

**Fala:**

> O EnergySim mostra onde pode existir desperdício, ajuda a entender seu impacto e permite comparar intervenções. Nossa próxima etapa seria conectar o modelo a medições reais e validar a detecção em diferentes computadores. Obrigado.

## O que a banca pode perguntar

**O sistema lê o consumo real do computador?**

Não. A versão apresentada é um simulador educativo baseado em perfis e modelos de consumo. A integração com telemetria real é um passo futuro.

**De onde vêm os 90 watts?**

É um valor controlado definido para construir um cenário de consumo extra visível e reproduzível. Não corresponde à medição de nenhum aplicativo específico.

**Por que considerar o resultado confiável dentro da simulação?**

Porque a tarefa principal, o perfil do computador e a carga útil de processamento permanecem iguais. A única mudança deliberada é a parcela extra de consumo. Os testes automatizados verificam essa condição e conferem a projeção de economia.

**O sistema otimiza o computador de verdade?**

Não. Ele executa uma intervenção no próprio modelo. Um produto real exigiria coleta de dados, verificação de processos e procedimentos seguros para sugerir ou aplicar alterações.

**Como é calculada a economia?**

Diferença de potência em kW multiplicada pelas horas de uso e pela tarifa: 0,09 kW × 240 h × R$ 0,90/kWh = R$ 19,44.

**Por que a temperatura muda?**

O modelo térmico estima a evolução da temperatura conforme a potência e a capacidade de resfriamento do computador simulado. Não se trata de termometria real.

## Checklist para o dia

1. Abra o terminal na pasta `EnergySim`.
2. Execute `pip install -r requirements.txt` uma vez, antecipadamente.
3. Inicie a aplicação com `python -m streamlit run app.py`.
4. Clique em **Recomeçar** antes da apresentação.
5. Use o navegador em tela cheia (F11), com zoom de 90% ou 100% conforme a resolução.
6. Ensaie os dois cliques principais até conseguir explicar o resultado sem ler a tela.
7. Não entre no modo completo durante a demonstração; reserve os detalhes para perguntas da banca.
8. Se a fonte de texto personalizada não carregar por falta de internet, o sistema utiliza uma fonte alternativa.
