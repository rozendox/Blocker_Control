"""
fixme -> atualizações



"""

import socket

# Configuração do cliente receptor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65531  # Porta do servidor


def confirmar_entrega(receptor_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    receptor_socket.send(f"CONFIRM DELIVERY|{nome_item}|{id_local}".encode())


def main():
    receptor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receptor_socket.connect((SERVER_HOST, SERVER_PORT))

    # Recebe a mensagem de boas-vindas do servidor
    print(receptor_socket.recv(1024).decode())

    while True:
        print("\n===== MENU DO RECEPTOR =====")
        print("1. Confirmar entrega de item")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            confirmar_entrega(receptor_socket)
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

        # Recebe a resposta do servidor para a operação executada
        resposta = receptor_socket.recv(1024).decode()
        print(f"Resposta do servidor: {resposta}")

    receptor_socket.close()


if __name__ == "__main__":
    main()
