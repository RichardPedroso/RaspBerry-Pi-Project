# Apresentação do Projeto Raspberry Pi

Este projeto visa implementar um sistema de medição utilizando um Raspberry Pi, focando na sustentabilidade e na minimização da pegada de carbono através do uso eficiente de tecnologias.

## Fórmula de Cálculo da Pegada de Carbono
A fórmula utilizada para o cálculo da pegada de carbono é definida como:

\[ \text{pegada de carbono (kg CO2)} = \frac{\text{potencia consumida (watts)} \times \text{tempo de operação (segundos)}}{3600} \times \text{fator de emissão regional (kg CO2/kWh)} \ \]

Com um fator de emissão regional do Brasil de **0,0917 kg CO2 por kWh**.

## Transmissão de Dados com SCP e Segurança
Os dados coletados são transmitidos ao Grupo 2 (Grupo de Firewall) utilizando o protocolo SCP (Secure Copy Protocol). Para garantir a segurança dos dados, implementamos um túnel de segurança utilizando hash SHA256.

## Ciclos de Medição
O sistema realiza ciclos de medição, onde cada ciclo contém **6 coletas** realizadas com três sensores diferentes:
1. Sensor de toque/presença
2. Sensor de temperatura
3. Sensor de luminosidade

As medições coletadas são registradas e utilizadas para o cálculo conjunto da pegada de carbono conforme descrito na fórmula mencionada anteriormente.