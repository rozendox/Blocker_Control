"""import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65535

def main():
    gerente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gerente_socket.connect((SERVER_HOST, SERVER_PORT))

    print(gerente_socket.recv(1024).decode())  # Recebe a mensagem de boas-vindas do servidor

    while True:
        # Recebe mensagens contínuas do servidor
        mensagem = gerente_socket.recv(1024).decode()
        print(f"Alerta do servidor: {mensagem}")

if __name__ == "__main__":
    main()
"""


import socket
import threading
import time

# Configuração do cliente gerente
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65535


def exibir_menu():
    print("\n===== MENU DO GERENTE =====")
    print("1. Adicionar item")
    print("2. Cadastrar local")
    print("3. Associar item a local")
    print("4. Enviar item")
    print("5. Listar itens enviados")
    print("6. Listar locais cadastrados")
    print("7. Associar etiquetas a objetos")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha


def adicionar_item(gerente_socket):
    nome_item = input("Nome do item: ")
    quantidade = input("Quantidade: ")
    gerente_socket.send(f"ADD ITEM|{nome_item}|{quantidade}".encode())


def cadastrar_local(gerente_socket):
    id_local = input("ID do local: ")
    nome_local = input("Nome do local: ")
    gerente_socket.send(f"REGISTER LOCATION|{id_local}|{nome_local}".encode())


def associar_item_local(gerente_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    gerente_socket.send(f"LINK ITEM TO LOCATION|{nome_item}|{id_local}".encode())


def enviar_item(gerente_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    quantidade = input("Quantidade: ")
    etiquetas = []
    for i in range(int(quantidade)):
        etiqueta = input(f"Digite o número da etiqueta para o item {i + 1}: ")
        etiquetas.append(etiqueta)
    etiquetas_str = ",".join(etiquetas)
    gerente_socket.send(f"SEND ITEM|{nome_item}|{id_local}|{quantidade}|{etiquetas_str}".encode())


def listar_itens_enviados(gerente_socket):
    gerente_socket.send("LIST SENT ITEMS".encode())


def listar_locais(gerente_socket):
    gerente_socket.send("LIST LOCATIONS".encode())


def associar_etiquetas(gerente_socket):
    nome_item = input("Nome do item: ")
    quantidade = int(input("Quantidade de itens: "))
    etiquetas = []
    for i in range(quantidade):
        etiqueta = input(f"Digite o número da etiqueta para o item {i + 1}: ")
        etiquetas.append(etiqueta)
    etiquetas_str = ",".join(etiquetas)
    gerente_socket.send(f"LINK TAGS|{nome_item}|{etiquetas_str}".encode())


def receber_alertas(gerente_socket):
    while True:
        mensagem = gerente_socket.recv(1024).decode()
        print(f"\nALERTA DO SERVIDOR: {mensagem}")


def main():
    gerente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gerente_socket.connect((SERVER_HOST, SERVER_PORT))

    # Recebe a mensagem de boas-vindas do servidor
    print(gerente_socket.recv(1024).decode())

    # Inicia uma thread para receber alertas de itens entregues incorretamente
    alert_thread = threading.Thread(target=receber_alertas, args=(gerente_socket,))
    alert_thread.daemon = True  # Thread daemon para encerrar junto com o programa
    alert_thread.start()

    while True:
        escolha = exibir_menu()

        if escolha == '1':
            adicionar_item(gerente_socket)
        elif escolha == '2':
            cadastrar_local(gerente_socket)
        elif escolha == '3':
            associar_item_local(gerente_socket)
        elif escolha == '4':
            enviar_item(gerente_socket)
        elif escolha == '5':
            listar_itens_enviados(gerente_socket)
        elif escolha == '6':
            listar_locais(gerente_socket)
        elif escolha == '7':
            associar_etiquetas(gerente_socket)
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

        resposta = gerente_socket.recv(1024).decode()
        print(f"Resposta do servidor: {resposta}")

    gerente_socket.close()


if __name__ == "__main__":
    main()
