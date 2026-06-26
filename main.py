import tkinter as tk
from tkinter import scrolledtext, messagebox
import serial
import threading
import time

# --- CONFIGURAÇÕES ---
PORTA_SERIAL = 'COM6' 
BAUD_RATE = 115200

class DestinationAgreementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador: Acordo no Destino (PC <-> ESP32)")
        self.root.geometry("600x450")

        self.local_clock = 0
        self.msg_counter = 1
        self.serial_conn = None

        self.setup_ui()
        self.conectar_serial()

    def setup_ui(self):
        tk.Label(self.root, text="Nó 1 (Computador)", font=("Arial", 14, "bold")).pack(pady=10)

        # --- FRAME PARA OS DOIS BOTÕES ---
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        # Botão Instantâneo (Modo 0)
        self.btn_instantaneo = tk.Button(frame_botoes, text="Enviar Instantâneo (Auto)", 
                                  command=lambda: self.propor_mensagem(0), bg="lightgreen", font=("Arial", 11))
        self.btn_instantaneo.grid(row=0, column=0, padx=10)

        # Botão Assíncrono (Modo 1)
        self.btn_assincrono = tk.Button(frame_botoes, text="Enviar Assíncrono (Espera Botão)", 
                                  command=lambda: self.propor_mensagem(1), bg="lightcoral", font=("Arial", 11))
        self.btn_assincrono.grid(row=0, column=1, padx=10)

        # --- LOG ---
        tk.Label(self.root, text="Log do Algoritmo:").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(self.root, width=65, height=15, state='disabled')
        self.log_area.pack(pady=5, padx=20)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def conectar_serial(self):
        try:
            self.serial_conn = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
            self.log(f"[SISTEMA] Conectado ao ESP32 na porta {PORTA_SERIAL}.")
            
            self.listen_thread = threading.Thread(target=self.escutar_esp32, daemon=True)
            self.listen_thread.start()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar na porta {PORTA_SERIAL}.")
            self.log(f"[ERRO] Falha ao conectar: {e}")

    def propor_mensagem(self, modo):
        if not self.serial_conn or not self.serial_conn.is_open:
            self.log("[ERRO] Serial não conectada.")
            return

        self.local_clock += 1
        msg_id = self.msg_counter
        self.msg_counter += 1

        # NOVO PROTOCOLO: Adiciona o modo no final da string (0 ou 1)
        pacote = f"PROPOSE|{msg_id}|{self.local_clock}|{modo}\n"
        
        modo_texto = "Instantâneo" if modo == 0 else "Assíncrono"
        self.log(f"-> [PROPOSTA] Msg ID: {msg_id} | Timestamp: {self.local_clock} | Modo: {modo_texto}")
        
        self.serial_conn.write(pacote.encode('utf-8'))

    def escutar_esp32(self):
        while True:
            if self.serial_conn and self.serial_conn.in_waiting > 0:
                try:
                    linha = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if linha == "ESP32_READY":
                        self.log("[ESP32] Placa reiniciada e pronta.")
                        
                    elif linha.startswith("AGREE|"):
                        partes = linha.split("|")
                        if len(partes) == 3:
                            msg_id = int(partes[1])
                            final_timestamp = int(partes[2])
                            
                            self.local_clock = max(self.local_clock, final_timestamp) + 1
                            
                            self.log(f"<- [ACORDO FEITO] Msg ID: {msg_id} aprovada pelo ESP32.")
                            self.log(f"   [ENTREGA] Mensagem {msg_id} entregue. Novo Relógio: {self.local_clock}\n")
                            
                except Exception as e:
                    pass # Ignora erros de leitura de lixo na serial
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = DestinationAgreementGUI(root)
    root.mainloop()