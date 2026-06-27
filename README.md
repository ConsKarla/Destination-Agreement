# Destination Agreement

## Visão Geral

O projeto **Destination Agreement** apresenta uma implementação prática
de conceitos de **Sistemas Distribuídos**, utilizando comunicação entre
um computador e uma placa **ESP32** para simular um mecanismo de acordo
e confirmação de entrega de mensagens.

A proposta principal é demonstrar como dois nós independentes podem
coordenar eventos utilizando mensagens, confirmação de recebimento e
sincronização através de relógios lógicos.

O sistema é composto por:

-    **Nó 1 - Computador:** aplicação Python responsável pelo envio
    das propostas e visualização dos eventos.
-    **Nó 2 - ESP32:** dispositivo embarcado responsável pelo
    processamento das mensagens e confirmação do acordo.

------------------------------------------------------------------------

#  Objetivos

O projeto tem como objetivos:

-   Implementar comunicação entre dois dispositivos através de
    comunicação serial.
-   Demonstrar o conceito de acordo entre nós distribuídos.
-   Aplicar conceitos de ordenação de eventos utilizando relógio lógico.
-   Comparar comportamentos síncronos e assíncronos.
-   Integrar software desenvolvido em Python com hardware embarcado.

------------------------------------------------------------------------

# Arquitetura do Sistema

    +-----------------------+
    |       Computador      |
    |                       |
    | Python + Tkinter GUI  |
    |          Nó 1         |
    +-----------+-----------+
                |
                |
          Comunicação Serial
            115200 bps
                |
                |
    +-----------+-----------+
    |          ESP32        |
    |                       |
    | Processamento         |
    | Controle físico       |
    |          Nó 2         |
    +-----------------------+

------------------------------------------------------------------------

# Tecnologias Utilizadas

## Software

-   Python 3
-   Tkinter para interface gráfica
-   PySerial para comunicação serial
-   Arduino IDE para programação do ESP32

## Hardware

-   ESP32
-   LED integrado
-   Botão físico para confirmação manual

------------------------------------------------------------------------

# Estrutura do Projeto

    Destination-Agreement/
    │
    ├── README.md
    │
    ├── main.py
    │   └── Aplicação gráfica do computador
    │
    └── sketch_jun23a.ino
        └── Código embarcado do ESP32

------------------------------------------------------------------------

# Funcionamento do Sistema

O computador inicia uma comunicação com o ESP32 através da porta serial.

A aplicação permite enviar mensagens utilizando dois modos:

## 1. Acordo Instantâneo

Neste modo, a mensagem é enviada ao ESP32 e aprovada automaticamente.

Fluxo:

    Computador
        |
        | PROPOSE
        ↓
     ESP32
        |
        | AGREE
        ↓
    Computador

------------------------------------------------------------------------

## 2. Acordo Assíncrono

Neste modo, o ESP32 recebe a mensagem, porém aguarda uma confirmação
externa através do botão físico.

Fluxo:

    Computador
        |
        | PROPOSE
        ↓
     ESP32
        |
     Aguarda botão
        |
        ↓
     AGREE
        |
    Computador

Esse modo representa uma situação onde a decisão depende de um evento
externo ao sistema computacional.

------------------------------------------------------------------------

# Protocolo de Comunicação

As mensagens seguem um protocolo simples baseado em texto.

## Envio da proposta

Formato:

    PROPOSE|ID|TIMESTAMP|MODE

Exemplo:

    PROPOSE|1|5|0

Significado:

  Campo       Descrição
  ----------- ---------------------------
  ID          Identificador da mensagem
  TIMESTAMP   Relógio lógico do emissor
  MODE        Tipo de acordo

------------------------------------------------------------------------

## Resposta de confirmação

Formato:

    AGREE|ID|TIMESTAMP

Exemplo:

    AGREE|1|6

Indica que a mensagem foi aceita e entregue.

------------------------------------------------------------------------

# Relógio Lógico

Para manter uma ordem dos eventos entre os dispositivos, o projeto
utiliza uma adaptação do **Relógio de Lamport**.

A atualização segue:

    Cnovo = max(Clocal, Crecebido) + 1

Essa técnica permite ordenar eventos distribuídos sem depender de um
relógio físico compartilhado.

------------------------------------------------------------------------

#  Interface Gráfica

A aplicação Python apresenta:

-   Conexão automática com ESP32.
-   Botão para envio instantâneo.
-   Botão para envio assíncrono.
-   Área de logs do sistema.
-   Monitoramento das mensagens recebidas.

Exemplo de execução:

    [SISTEMA] Conectado ao ESP32

    -> PROPOSTA
    Mensagem: 1
    Timestamp: 2
    Modo: Instantâneo

    <- ACORDO FEITO

    Mensagem entregue.
    Novo relógio: 4

------------------------------------------------------------------------

# Fluxo Geral do Algoritmo

1.  Usuário seleciona o tipo de acordo.
2.  Computador incrementa seu relógio lógico.
3.  Uma mensagem PROPOSE é enviada ao ESP32.
4.  ESP32 recebe e processa a solicitação.
5.  O relógio lógico é atualizado.
6.  O ESP32 envia a confirmação AGREE.
7.  Computador registra a entrega.

------------------------------------------------------------------------

# Resultados Esperados

Com a execução do projeto é possível observar:

✅ Comunicação entre processos distribuídos\
✅ Troca de mensagens entre dispositivos\
✅ Sincronização através de relógios lógicos\
✅ Diferença entre eventos síncronos e assíncronos\
✅ Integração entre aplicação desktop e sistema embarcado

------------------------------------------------------------------------

# Como Executar

## ESP32

1.  Abrir o arquivo:

```{=html}
<!-- -->
```
    sketch_jun23a.ino

2.  Compilar e enviar para a placa ESP32.

Configuração serial:

    Baud Rate: 115200

------------------------------------------------------------------------

## Python

Instalar dependência:

``` bash
pip install pyserial
```

Executar:

``` bash
python main.py
```

------------------------------------------------------------------------

# Conceitos Aplicados

-   Sistemas Distribuídos
-   Comunicação Serial
-   Message Passing
-   Relógios Lógicos
-   Ordenação de Eventos
-   Sistemas Embarcados
-   Comunicação Hardware-Software

------------------------------------------------------------------------

# Conclusão

O projeto demonstra uma aplicação prática dos conceitos estudados em
sistemas distribuídos, mostrando como dispositivos independentes podem
estabelecer acordos, trocar informações e manter uma ordem consistente
de eventos.

A integração entre Python e ESP32 permite visualizar, de forma
experimental, problemas clássicos de comunicação distribuída e suas
soluções utilizando protocolos simples e mecanismos de sincronização.
