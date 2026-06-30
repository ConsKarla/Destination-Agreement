# Destination Agreement (Acordo no Destino)

**Universidade Federal de Santa Catarina (UFSC) - Campus Araranguá**

**Curso:** Engenharia de Computação

## Visão Geral

O projeto **Destination Agreement** apresenta uma implementação prática de conceitos de **Sistemas Distribuídos**, utilizando comunicação serial entre um microcontrolador **ESP32** e um computador para simular um mecanismo de acordo e confirmação de entrega de mensagens baseada em Relógios Lógicos de Lamport.

Para atender aos requisitos do algoritmo clássico de Acordo no Destino (que exige múltiplos nós para a ocorrência de um consenso), a arquitetura do sistema foi projetada de forma invertida e híbrida:

* **Cliente (ESP32):** Dispositivo embarcado responsável pela geração de eventos assíncronos (via hardware) e envio das propostas de mensagens para a rede.
* **Cluster Servidor (Computador):** Aplicação em Python que simula virtualmente **3 Nós de Destino Independentes (Servidores A, B e C)**. Eles recebem a proposta, atualizam seus relógios lógicos individuais, realizam o consenso matemático (Acordo) e devolvem a confirmação unificada ao cliente.

---

## Objetivos

* Implementar comunicação assíncrona entre software (Python) e hardware (ESP32).
* Demonstrar o conceito de consenso (Acordo no Destino) entre múltiplos nós distribuídos.
* Aplicar a ordenação de eventos e sincronização causal utilizando o **Relógio Lógico de Lamport**.
* Desenvolver uma interface gráfica moderna para monitoramento de logs e estados dos nós em tempo real.

---

## Arquitetura do Sistema

```text
    +-----------------------+
    |         ESP32         |
    |    (Nó Emissor)       |
    |                       |
    | - Botão (Gera Evento) |
    | - LED (Estado Espera) |
    +-----------+-----------+
                |
                | Comunicação Serial (USB)
                | PROPOSE / AGREE (115200 bps)
                |
    +-----------+---------------------------------+
    |               COMPUTADOR                    |
    |        (Cluster de Destino - Python)        |
    |                                             |
    |  +------------+ +------------+ +---------+  |
    |  | Servidor A | | Servidor B | |ServidorC|  |
    |  +------------+ +------------+ +---------+  |
    |         \             |             /       |
    |          \            |            /        |
    |           +-----------------------+         |
    |           | CONSENSO (Max Clock)  |         |
    |           +-----------------------+         |
    +---------------------------------------------+
```

---

## Tecnologias Utilizadas

### Software
* **Python 3:** Lógica de roteamento e servidores virtuais.
* **CustomTkinter:** Biblioteca para construção de Interface Gráfica moderna (Dark Mode).
* **PySerial:** Integração de comunicação serial USB.
* **Arduino IDE (C++):** Programação do firmware do ESP32.

### Hardware
* **ESP32:** Microcontrolador principal.
* **LED e Resistor:** Indicador visual de estado de latência/espera (Pino D2).
* **Push Button:** Acionador manual de eventos usando resistor interno de *pull-up* (Pino D4).

---

## Funcionamento do Sistema e Fluxo do Algoritmo

O sistema demonstra o tratamento de eventos assíncronos. A interação ocorre da seguinte forma:

1. **Geração do Evento:** O usuário pressiona o botão físico no ESP32.
2. **Proposta:** O ESP32 incrementa seu relógio lógico e envia uma mensagem `PROPOSE` via porta serial. O LED acende e o ESP32 entra em estado de bloqueio (aguardando o acordo).
3. **Processamento Distribuído:** O Computador recebe a proposta e a repassa para os 3 Servidores (A, B e C).
4. **Sincronização de Lamport:** Cada servidor atualiza seu próprio relógio baseado na fórmula: `Cnovo = max(Clocal, Crecebido) + 1`.
5. **O Acordo no Destino:** O sistema realiza o consenso selecionando o **maior timestamp** gerado entre os três nós, garantindo a ordenação matemática e determinística do evento.
6. **Confirmação:** O Computador envia a mensagem `AGREE` de volta ao ESP32 contendo o timestamp validado.
7. **Entrega:** O ESP32 recebe o acordo, atualiza seu próprio relógio, apaga o LED (sinalizando a entrega oficial da mensagem) e libera o sistema para um novo envio.

---

## Protocolo de Comunicação

O protocolo foi projetado em texto puro e os parâmetros são separados por *pipes* (`|`).

### Envio da Proposta (Cliente -> Servidor)
* **Formato:** `PROPOSE|ID|TIMESTAMP`
* **Exemplo:** `PROPOSE|1|5`
* **Descrição:** O Cliente solicita a entrega da mensagem de identificador `1`, com o seu relógio lógico atual em `5`.

### Resposta de Confirmação (Servidor -> Cliente)
* **Formato:** `AGREE|ID|TIMESTAMP_ACORDADO`
* **Exemplo:** `AGREE|1|6`
* **Descrição:** O Cluster Servidor confirma que o consenso foi atingido e o timestamp final da operação em toda a rede será `6`.

---

## Interface Gráfica (GUI)

A aplicação desktop foi modernizada com `CustomTkinter` e apresenta:
* Painel em tempo real exibindo os 3 Nós Servidores Virtuais e seus respectivos relógios lógicos.
* Terminal integrado de Logs detalhando cada etapa do consenso (recebimento, cálculo de Lamport em cada nó, acordo de valor máximo e resposta).

---

## Como Executar

### 1. Configuração do Hardware (ESP32)
1. Abra o código `sketch.ino` na **Arduino IDE**.
2. Conecte um LED ao pino **D2** (GPIO2) e um Push Button ao pino **D4** (GPIO4).
3. Compile e faça o upload para a placa.
4. *Importante:* Feche a Arduino IDE para liberar a porta Serial.

### 2. Configuração do Software (Computador)
1. Instale as dependências necessárias utilizando o terminal:
   ```bash
   pip install pyserial customtkinter
   ```
2. Verifique no arquivo `main.py` se a variável `PORTA_SERIAL` corresponde à porta conectada ao seu ESP32 (ex: `COM6`).
3. Execute a interface gráfica:
   ```bash
   python main.py
   ```

---

## Conclusão

Este projeto demonstra com sucesso a abstração e aplicação dos conceitos de Sistemas Distribuídos. A inversão da arquitetura tradicional permitiu criar um ambiente prático onde um único dispositivo IoT (ESP32) interage ativamente com um cluster simulado, validando na prática a exclusão mútua, a sincronização de relógios de Lamport e a eficácia de algoritmos de consenso diante de latências inseridas no mundo físico.
