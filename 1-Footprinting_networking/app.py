import os
import socket

# Usa variables de entorno para configurar el protocolo y los mensajes
KEY = os.getenv('KEY', 'DEFAULT_KEY')
SUCCESS = os.getenv('SUCCESS', b'Success').encode()
PROTOCOL = os.getenv('PROTOCOL', 'TCP')  # TCP es el valor por defecto

HOST = '0.0.0.0'
PORT = 80

if PROTOCOL.upper() == "UDP":
    socket_type = socket.SOCK_DGRAM
else:
    socket_type = socket.SOCK_STREAM

with socket.socket(socket.AF_INET, socket_type) as s:
    s.bind((HOST, PORT))
    print(f"Escuchando en {HOST}:{PORT} con {PROTOCOL}...")
    
    if PROTOCOL.upper() == "TCP":
        s.listen()
    
    while True:
        if PROTOCOL.upper() == "TCP":
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if data.decode() == KEY:
                    conn.sendall(SUCCESS)
                    print("Mensaje de éxito enviado, cerrando conexión.")
                    conn.close()
                else:
                    print("Datos incorrectos recibidos, cerrando conexión.")
                    conn.close()
        else:  # UDP
            data, addr = s.recvfrom(1024)
            print('Connected by', addr)
            if data.decode() == KEY:
                s.sendto(SUCCESS, addr)
                print("Mensaje de éxito enviado.")
            else:
                print("Datos incorrectos recibidos.")
