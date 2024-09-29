    import socket

    # Configuração do cliente
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 65535

    def exibir_menu():
        print("\n===== MENU DO NÓ CLIENTE =====")
        print("1. Adicionar item")
        print("2. Cadastrar local")
        print("3. Associar item a local")
        print("4. Enviar item")
        print("5. Confirmar entrega")
        print("6. Listar itens enviados")
        print("7. Listar locais cadastrados")
        print("8. Associar etiquetas a objetos")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")
        return escolha

    def adicionar_item(cliente_socket):
        nome_item = input("Nome do item: ")
        quantidade = input("Quantidade: ")
        cliente_socket.send(f"ADD ITEM|{nome_item}|{quantidade}".encode())

    def cadastrar_local(cliente_socket):
        id_local = input("ID do local: ")
        nome_local = input("Nome do local: ")
        cliente_socket.send(f"REGISTER LOCATION|{id_local}|{nome_local}".encode())

    def associar_item_local(cliente_socket):
        nome_item = input("Nome do item: ")
        id_local = input("ID do local: ")
        cliente_socket.send(f"LINK ITEM TO LOCATION|{nome_item}|{id_local}".encode())

    def enviar_item(cliente_socket):
        nome_item = input("Nome do item: ")
        id_local = input("ID do local: ")
        quantidade = input("Quantidade: ")
        etiquetas = []
        for i in range(int(quantidade)):
            etiqueta = input(f"Digite o número da etiqueta para o item {i+1}: ")
            etiquetas.append(etiqueta)
        etiquetas_str = ",".join(etiquetas)
        cliente_socket.send(f"SEND ITEM|{nome_item}|{id_local}|{quantidade}|{etiquetas_str}".encode())

    def confirmar_entrega(cliente_socket):
        nome_item = input("Nome do item: ")
        id_local = input("ID do local: ")
        cliente_socket.send(f"CONFIRM DELIVERY|{nome_item}|{id_local}".encode())

    def listar_itens_enviados(cliente_socket):
        cliente_socket.send("LIST SENT ITEMS".encode())

    def listar_locais(cliente_socket):
        cliente_socket.send("LIST LOCATIONS".encode())

    def associar_etiquetas(cliente_socket):
        nome_item = input("Nome do item: ")
        quantidade = int(input("Quantidade de itens: "))
        etiquetas = []
        for i in range(quantidade):
            etiqueta = input(f"Digite o número da etiqueta para o item {i+1}: ")
            etiquetas.append(etiqueta)
        etiquetas_str = ",".join(etiquetas)
        cliente_socket.send(f"LINK TAGS|{nome_item}|{etiquetas_str}".encode())

    def main():
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((SERVER_HOST, SERVER_PORT))

        print(cliente_socket.recv(1024).decode())  # Recebe a mensagem de boas-vindas do servidor

        while True:
            escolha = exibir_menu()

            if escolha == '1':
                adicionar_item(cliente_socket)
            elif escolha == '2':
                cadastrar_local(cliente_socket)
            elif escolha == '3':
                associar_item_local(cliente_socket)
            elif escolha == '4':
                enviar_item(cliente_socket)
            elif escolha == '5':
                confirmar_entrega(cliente_socket)
            elif escolha == '6':
                listar_itens_enviados(cliente_socket)
            elif escolha == '7':
                listar_locais(cliente_socket)
            elif escolha == '8':
                associar_etiquetas(cliente_socket)
            elif escolha == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

            resposta = cliente_socket.recv(1024).decode()
            print(f"Resposta do servidor: {resposta}")

        cliente_socket.close()

    if __name__ == "__main__":
        main()
