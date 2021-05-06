# Importação das bibliotecas.
import socket
import select


def broadcast(msg):
    # Manda mensagem para todos os sockets conectados, menos para o servidor.
    for sock in CONNECTION_LIST:
        if sock != server_socket:
            try:
                sock.sendall(msg)  # Envia todas as mensagem de uma vez.
            except Exception as mensagem:  # Conexão encerrada/erro.
                print(type(mensagem).__name__)
                sock.close()
                try:
                    CONNECTION_LIST.remove(sock)
                except ValueError as mensagem:
                    print("{}:{}".format(type(mensagem).__name__, mensagem))


CONNECTION_LIST = []
RECV_BUFFER = 4096  # Valores comuns são potências de 2, como 4096 ou 8192.
PORT = 1331

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))  # string de endereço vazia significa INADDR_ANY (sem saber o endereço IP).

print("Aguardando a conexão dos clientes...")  # O servidor fica escutando.
server_socket.listen(10)  # Até 10 clientes podem se conectarem.

CONNECTION_LIST.append(server_socket)  # Adiciona o socket do servidor à lista de conexões legíveis.
print("Servidor inicializado.")

while True:
    # Pega a lista de sockets que estão prontos para serem lidos pelo select.
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(CONNECTION_LIST, [], [])
    for SOCK in READ_SOCKETS:  # Nova conexão
        # Lida com o caso em que há uma nova conexão recebida através do server_socket.
        if SOCK == server_socket:
            SOCKFD, ADDR = server_socket.accept()
            CONNECTION_LIST.append(SOCKFD)  # Adciona um socket descritor.
            # Adicionando \ r para impedir a sobreposição de mensagens quando outro usuário escreve a mensagem.
            print("\r({0}, {1}) se conectou".format(ADDR[0], ADDR[1]))
            broadcast("({0}:{1}) entrou na sala\n"
                      .format(ADDR[0], ADDR[1]).encode())
        else:  # Alguma mensagem recebida de um cliente.
            try:  # Processa o dado recebido do cliente.
                DATA = SOCK.recv(RECV_BUFFER)
                if DATA:
                    ADDR = SOCK.getpeername()  # Obtem o endereço remoto do socket.
                    msg = "\r[{}:{}]: {}".format(ADDR[0], ADDR[1], DATA.decode())
                    print(msg, end="")
                    broadcast(msg.encode())
            except Exception as mensagem:  # Erro, cliente desconectou.
                print(type(mensagem).__name__, mensagem)
                print("\r({0}, {1}) desconectou.".format(ADDR[0], ADDR[1]))
                broadcast("\r({0}, {1}) ficou offline.\n"
                          .format(ADDR[0], ADDR[1]).encode())
                SOCK.close()
                try:
                    CONNECTION_LIST.remove(SOCK)
                except ValueError as mensagem:
                    print("{}:{}.".format(type(mensagem).__name__, mensagem))
                continue

server_socket.close()
