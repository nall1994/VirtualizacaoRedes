import socket
import json

def mainmenu():
    switcher = {
        1: list_files,
        2: file_request
    }
    while True:
        print("\n")
        print("----- MENU -----")
        print("----- 1 - Listar ficheiros disponíveis")
        print("----- 2 - Transferir ficheiro")
        print("----- 3 - Sair")
        escolha = input("Insira a sua opção: ")
        try:
            escolha = int(escolha)
            if escolha < 1 or escolha > 3:
                print("\n")
                print("A escolha tem que ser um número inteiro entre 1 e 3 inclusive.")
            else:
                print("\n")
                function_to_execute = switcher.get(escolha,None)
                function_to_execute()
        except ValueError:
            print("\n")
            print("A escolha tem que ser um número inteiro entre 1 e 3 inclusive.")

def list_files():
    sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    message = {
        "type" : "LIST_FILES"
    }
    message = json.dumps(message).encode('utf8')
    sending_socket.sendto(message,('''ipAnycast''', 10002))
    # Receber a informação da listagem de ficheiros e imprimir no ecrã.
    # É preciso fazer json.loads(message.decode('utf8'))

def file_request():
    sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    file_name = input("Insira o nome do ficheiro que pretende transferir: ")
    message = {
        "type" : "FILE_REQUEST",
        "file_name" : file_name
    }
    message = json.dumps(message).encode('utf8')
    sending_socket.sendto(message,('''ipAnycast''', 10002))
    #enviar mensagem

