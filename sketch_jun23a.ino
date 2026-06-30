#include <Arduino.h>

const int LED_PIN = 2;
const int BOTAO_PIN = 4;

int local_clock = 0;
int msg_counter = 1;
bool aguardando_acordo = false; // espera servidor responder

void setup() {
    pinMode(LED_PIN, OUTPUT);
    pinMode(BOTAO_PIN, INPUT_PULLUP);
    
    Serial.begin(115200);
    while (!Serial) {;} // roda até o serial ficar 100% pronto
    Serial.println("ESP32_CLIENT_READY");
}

void loop() {
    // 1. CLIENTE GERA A MENSAGEM (Ao apertar o botão físico)
    if (digitalRead(BOTAO_PIN) == LOW && !aguardando_acordo) {
        
        local_clock++; // Incrementa relógio antes de enviar
        int msg_id = msg_counter;
        msg_counter++;

        // Envia a proposta para os 3 Servidores no PC
        Serial.print("PROPOSE|");
        Serial.print(msg_id);
        Serial.print("|");
        Serial.println(local_clock);

        digitalWrite(LED_PIN, HIGH); // acende o LED
        aguardando_acordo = true;    // trava para não mandar 100 mensagens de uma vez
        
        delay(300);
    }

    // recebe a resposta
    if (Serial.available() > 0 && aguardando_acordo) {
        String incomingMessage = Serial.readStringUntil('\n'); // le até \n
        incomingMessage.trim(); // limpa mensagem

        if (incomingMessage.startsWith("AGREE|")) {
            int p1 = incomingMessage.indexOf('|');
            int p2 = incomingMessage.indexOf('|', p1 + 1);
            
            int msg_id = incomingMessage.substring(p1 + 1, p2).toInt();
            int agreed_timestamp = incomingMessage.substring(p2 + 1).toInt();

            // atualiza relógio
            local_clock = max(local_clock, agreed_timestamp) + 1;

            // apaga led
            digitalWrite(LED_PIN, LOW);
            aguardando_acordo = false; // libera para apertar o botão novamente
        }
    }
}
