"""
fixme -> atualizações------



"""


import socket
import threading

# Configuração do cliente gerente
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65531  # Porta para gerente

# Variável global para controlar o recebimento de alertas
receber_alertas_ativo = False

def exibir_menu():
    print("\n===== MENU DO GERENTE =====")
    print("1. Adicionar item")
    print("2. Cadastrar local")
    print("3. Associar item a local")
    print("4. Enviar item")
    print("5. Listar itens enviados")
    print("6. Listar locais cadastrados")
    print("7. Associar etiquetas a objetos")
    print("8. Ativar/Desativar recebimento de mensagens")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha

def adicionar_item(gerente_socket):
    nome_item = input("Nome do item: ")
    quantidade = input("Quantidade: ")
    gerente_socket.send(f"ADD ITEM|{nome_item}|{quantidade}".encode())
    receber_resposta(gerente_socket)

def cadastrar_local(gerente_socket):
    id_local = input("ID do local: ")
    nome_local = input("Nome do local: ")
    gerente_socket.send(f"REGISTER LOCATION|{id_local}|{nome_local}".encode())
    receber_resposta(gerente_socket)

def associar_item_local(gerente_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    gerente_socket.send(f"LINK ITEM TO LOCATION|{nome_item}|{id_local}".encode())
    receber_resposta(gerente_socket)

def enviar_item(gerente_socket):
    nome_item = input("Nome do item: ")
    id_local = input("ID do local: ")
    quantidade = input("Quantidade: ")
    gerente_socket.send(f"SEND ITEM|{nome_item}|{id_local}|{quantidade}".encode())
    receber_resposta(gerente_socket)

def listar_itens_enviados(gerente_socket):
    gerente_socket.send("LIST SENT ITEMS".encode())
    receber_resposta(gerente_socket)

def listar_locais(gerente_socket):
    gerente_socket.send("LIST LOCATIONS".encode())
    receber_resposta(gerente_socket)

def receber_resposta(gerente_socket):
    resposta = gerente_socket.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")

# Função que será executada em uma thread separada para receber alertas do servidor
def receber_alertas(gerente_socket):
    while receber_alertas_ativo:
        try:
            mensagem = gerente_socket.recv(1024).decode()
            if mensagem:
                print(f"\nALERTA DO SERVIDOR: {mensagem}")
        except:
            print("Erro ao receber alertas.")
            break

def alternar_recebimento_alertas(gerente_socket):
    global receber_alertas_ativo
    if receber_alertas_ativo:
        receber_alertas_ativo = False
        print("Recebimento de mensagens desativado.")
    else:
        receber_alertas_ativo = True
        print("Recebimento de mensagens ativado.")
        # Inicia uma thread para receber alertas de itens entregues incorretamente ou itens não cadastrados
        alert_thread = threading.Thread(target=receber_alertas, args=(gerente_socket,))
        alert_thread.daemon = True  # Thread daemon para encerrar junto com o programa
        alert_thread.start()

def main():
    gerente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        gerente_socket.connect((SERVER_HOST, SERVER_PORT))
        # Recebe a mensagem de boas-vindas do servidor
        print(gerente_socket.recv(1024).decode())

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
                print("Funcionalidade em desenvolvimento.")
            elif escolha == '8':
                alternar_recebimento_alertas(gerente_socket)
            elif escolha == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor em {SERVER_HOST}:{SERVER_PORT}")
    finally:
        gerente_socket.close()

if __name__ == "__main__":
    main()
