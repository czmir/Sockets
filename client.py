# Importação das bibliotecas.
import socket
import select
import sys

# sys.argv é uma lista em Python, que contém os argumentos
# da linha de comando passados para o script.
if len(sys.argv) < 3:
    print("Para conexão no localhost utilize: 127.0.0.1 1331".format(sys.argv[0]))
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

# Cria o socket, sendo AF_INET o IPV4 e o SOCK_STREAM o protocolo TCP.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(200)

# Conecta com o host.
try:
    client_socket.connect((HOST, PORT))
except Exception as msg:
    print(type(msg).__name__)
    print("Erro ao conectar.")
    sys.exit()

print("Conectado ao host.")
print("Chat iniciado!")

while True:
    SOCKET_LIST = [sys.stdin, client_socket]
    # Pega uma lista de socket para ler.
    # Obtém os sockets da lista que são legíveis.
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    for sock in READ_SOCKETS:  # Mensagem recebida do servidor remoto.
        if sock == client_socket:
            data = sock.recv(4096)
            if not data:
                print('\nDesconectado do chat.')
                sys.exit()
            else:  # Escreve o dado.
                print(data.decode(), end=" ")
        else:  # Usuário entra com a mensagem.
            msg = sys.stdin.readline()
            print("\x1b[1A" + "\x1b[2K", end=" ")  # "\x1b" equivale a tecla Esc e "[2K" apaga a linha.
            client_socket.sendall(msg.encode())
