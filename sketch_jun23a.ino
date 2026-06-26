#include <Arduino.h>

// --- PINOS ---
const int LED_PIN = 2;    // Pino do LED
const int BOTAO_PIN = 4;  // Pino do Botão (com resistor interno)

// --- VARIÁVEIS DO ALGORITMO ---
int local_clock = 0;
bool mensagem_pendente = false;
int msg_id_pendente = 0;

void setup() {
    pinMode(LED_PIN, OUTPUT);
    pinMode(BOTAO_PIN, INPUT_PULLUP); 
    
    Serial.begin(115200);
    while (!Serial) {;}
    Serial.println("ESP32_READY");
}

void loop() {
    // 1. RECEBE NOVA MENSAGEM DO PC
    if (Serial.available() > 0 && !mensagem_pendente) {
        String incomingMessage = Serial.readStringUntil('\n');
        incomingMessage.trim(); 

        if (incomingMessage.startsWith("PROPOSE|")) {
            // Separa os dados pelos divisores "|"
            int p1 = incomingMessage.indexOf('|');
            int p2 = incomingMessage.indexOf('|', p1 + 1);
            int p3 = incomingMessage.indexOf('|', p2 + 1);
            
            int msg_id = incomingMessage.substring(p1 + 1, p2).toInt();
            int proposed_timestamp = incomingMessage.substring(p2 + 1, p3).toInt();
            int modo = incomingMessage.substring(p3 + 1).toInt(); // 0 = Instantâneo, 1 = Botão

            // Lógica de Lamport (Sincronização do Acordo)
            local_clock = max(local_clock, proposed_timestamp) + 1;

            // ACENDE O LED
            digitalWrite(LED_PIN, HIGH);

            if (modo == 1) {
                // MODO ASSÍNCRONO: Trava e espera o botão
                mensagem_pendente = true;
                msg_id_pendente = msg_id;
            } else {
                // MODO INSTANTÂNEO: Devolve a mensagem imediatamente
                Serial.print("AGREE|");
                Serial.print(msg_id);
                Serial.print("|");
                Serial.println(local_clock);
                
                delay(50); 
                digitalWrite(LED_PIN, LOW); // Apaga o LED na hora
            }
        }
    }

    // 2. VERIFICA O BOTÃO (Apenas se houver mensagem pendente)
    if (mensagem_pendente) {
        if (digitalRead(BOTAO_PIN) == LOW) { 
            
            // Realiza o Acordo no Destino
            Serial.print("AGREE|");
            Serial.print(msg_id_pendente);
            Serial.print("|");
            Serial.println(local_clock);

            // APAGA O LED
            digitalWrite(LED_PIN, LOW);
            mensagem_pendente = false; 
            
            delay(300); // Debounce do botão
        }
    }
}