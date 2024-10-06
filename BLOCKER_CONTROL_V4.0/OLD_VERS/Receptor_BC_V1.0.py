import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65535

def confirmar_entrega(cliente_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    cliente_socket.send(f"CONFIRM DELIVERY|{nome_item}|{id_local}".encode())

def main():
    receptor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receptor_socket.connect((SERVER_HOST, SERVER_PORT))

    print(receptor_socket.recv(1024).decode())  # Recebe a mensagem de boas-vindas do servidor

    while True:
        confirmar_entrega(receptor_socket)

if __name__ == "__main__":
    main()
