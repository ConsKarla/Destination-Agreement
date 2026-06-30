import customtkinter as ctk
import serial
import threading
import time

# config
PORTA_SERIAL = 'COM6'
BAUD_RATE = 115200

# interface
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class ServidorNode:
    def __init__(self, nome):
        self.nome = nome
        self.clock = 0

    def receber_proposta(self, timestamp_proposto):
        # relógio de Lamport de cada nó
        self.clock = max(self.clock, timestamp_proposto) + 1
        return self.clock

class DestinationAgreementServerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cluster Servidor - Acordo no Destino")
        self.root.geometry("700x500")

        # Cria 3 nós
        self.nodes = [ServidorNode("Servidor A"), ServidorNode("Servidor B"), ServidorNode("Servidor C")]
        self.serial_conn = None

        self.setup_ui()
        self.conectar_serial()

    def setup_ui(self):
        # titulo
        self.lbl_title = ctk.CTkLabel(self.root, text="Servidores de Destino (Nós A, B e C)", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(pady=15)

        # painel com os nós
        self.frame_nodes = ctk.CTkFrame(self.root)
        self.frame_nodes.pack(pady=10, padx=20, fill="x")

        self.lbl_nodes = []
        for i, node in enumerate(self.nodes):
            lbl = ctk.CTkLabel(self.frame_nodes, text=f"{node.nome}\nRelógio: {node.clock}", font=ctk.CTkFont(size=14))
            lbl.grid(row=0, column=i, padx=40, pady=10)
            self.lbl_nodes.append(lbl)

        # log
        self.lbl_log = ctk.CTkLabel(self.root, text="Terminal de Consenso:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_log.pack(anchor="w", padx=20)
        
        self.log_area = ctk.CTkTextbox(self.root, width=650, height=250, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_area.pack(pady=5, padx=20)
        self.log_area.configure(state="disabled")
    # config dos logs
    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def atualizar_tela_clocks(self):
        for i, node in enumerate(self.nodes):
            self.lbl_nodes[i].configure(text=f"{node.nome}\nRelógio: {node.clock}")

    def conectar_serial(self):
        try:
            self.serial_conn = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
            self.log(f"[SISTEMA] Aguardando propostas do ESP32 na porta {PORTA_SERIAL}...")
            
            threading.Thread(target=self.escutar_esp32, daemon=True).start()
        except Exception as e:
            self.log(f"[ERRO] Falha ao conectar na porta {PORTA_SERIAL}. Verifique o cabo.")

    def escutar_esp32(self):
        while True:
            if self.serial_conn and self.serial_conn.in_waiting > 0:
                try:
                    linha = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if linha == "ESP32_CLIENT_READY":
                        self.log("\n[CLIENTE ESP32] Conectado e pronto para enviar mensagens.")
                        
                    elif linha.startswith("PROPOSE|"):
                        partes = linha.split("|")
                        if len(partes) == 3:
                            msg_id = int(partes[1])
                            timestamp_cliente = int(partes[2])
                            
                            self.log(f"\n>> [RECEBIDO] Proposta da Msg {msg_id} (Timestamp Cliente: {timestamp_cliente})")
                            
                            # nós recebem mensagem e atualizam relogio
                            clocks_propostos = []
                            for node in self.nodes:
                                novo_clock = node.receber_proposta(timestamp_cliente)
                                clocks_propostos.append(novo_clock)
                                self.log(f"   - {node.nome} processou. Clock local: {novo_clock}")
                            
                            # define maior timestamp
                            acordo_final = max(clocks_propostos)
                            self.log(f"<< [CONSENSO] Acordo atingido! Timestamp final será: {acordo_final}")
                            
                            # atualiza todos os relogios para o definido
                            for node in self.nodes:
                                node.clock = max(node.clock, acordo_final)
                            
                            # mostra na tela
                            self.root.after(0, self.atualizar_tela_clocks)

                            # responde o esp32
                            resposta = f"AGREE|{msg_id}|{acordo_final}\n"
                            self.serial_conn.write(resposta.encode('utf-8'))
                            self.log(f"   [ENTREGA] Resposta AGREE enviada ao Cliente.")
                            
                except Exception:
                    pass
            time.sleep(0.1)
# mantem interface rodando
if __name__ == "__main__":
    app = ctk.CTk()
    gui = DestinationAgreementServerUI(app)
    app.mainloop()
