"""
fixme -> atualizações------
    06/10/24
        introdução das GUI iniciais.





"""

import socket
import threading
import tkinter as tk

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
    print("6. Lister locais cadastrados")
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


"""
MAIN -> window - tk

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
                print("Opção invalida!")

    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor em {SERVER_HOST}:{SERVER_PORT}")
    finally:
        gerente_socket.close()
"""


def criar_janela():
    root = tk.Tk()
    root.title("Gerente by BC inc")

    # Adicionar item
    tk.Label(root, text="nome do item:").grid(row=0, column=0)
    global entry_item
    entry_item = tk.Entry(root)
    entry_item.grid(row=0, column=1)

    tk.Label(root, text="Quantidade:").grid(row=1, column=0)
    global entry_quantidade
    entry_quantidade = tk.Entry(root)
    entry_quantidade.grid(row=1, column=1)

    btn_adicionar_item = tk.Button(root, text="Adicionar", command=adicionar_item)
    btn_adicionar_item.grid(row=2, column=1)

    # bora cadastrar local

    tk.Label(root, text="ID do local:").grid(row=3, column=0)
    global entry_id_local
    entry_id_local = tk.Entry(root)
    entry_id_local.grid(row=3, column=1)

    tk.Label(root, text="Nome do local:").grid(row=4, column=0)
    global entry_nome_local
    entry_nome_local = tk.Entry(root)
    entry_nome_local.grid(row=4, column=1)

    btn_cadastrar_local = tk.Button(root, text="Cadastrar local:", command=cadastrar_local)
    btn_cadastrar_local.grid(row=5, column=1)

    # Bora associar um item a um local de criiiiiiiiiiiiiiiiiiiiiiiiia
    btn_associar_item = tk.Button(root, text="Associar item a Local", command=associar_item_local)
    btn_associar_item.grid(row=6, column=1)

    #enviar itemmmmmmmmmm, mas é de cria?
    btn_enviar_item = tk.Button(root, text="Enviar item", command=enviar_item)
    btn_enviar_item.grid(row=7, column=1)

    #bora listar a cria que os cria enviou pro cria dos cria?
    btn_listar_itens = tk.Button(root, text="listar itens enviados", command=listar_itens_enviados)
    btn_listar_itens.grid(row=8, column=1)

    # bora listar agora os locais cadastrados? como tu vai se achar na criolandia sem saber o que tem?
    btn_listar_locais = tk.Button(root, text="listar locais", command=listar_locais)
    btn_listar_locais.grid(row=9, column=1)

    # esse aqui eu vou codar, mas vai ficar pra funcionar em segunda instancia
    # recebimento de alertas, futuramente desativado será
    btn_alertas = tk.Button(root, text="Ativar/Desativar alertas", command=alternar_recebimento_alertas)
    btn_alertas.grid(row=10, column=1)

    """# cria que é cria se conecta, num é memo?
    btn_conectar = tk.Button(root, text="Connectar ao servidor", command=conectar_servidor)
    btn_conectar.grid(row = 11, column = 1)"""

    root.mainloop()


if __name__ == "__main__":
    criar_janela()
