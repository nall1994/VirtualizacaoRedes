# coding=utf-8

import socket
import json
import sys
import os

def mainmenu():
    switcher = {
        1: list_files,
        2: file_request,
        3: file_upload,
        4: system_exit
    }
    while True:
        print("\n")
        print("----- MENU -----")
        print("----- 1 - Listar ficheiros disponíveis")
        print("----- 2 - Transferir ficheiro")
        print("----- 3 - Upload de ficheiro")
        print("----- 4 - Sair")
        escolha = input("Insira a sua opção: ")
        try:
            escolha = int(escolha)
            if escolha < 1 or escolha > 4:
                print("\n")
                print("A escolha tem que ser um número inteiro entre 1 e 4 inclusive.")
            else:
                print("\n")
                function_to_execute = switcher.get(escolha,None)
                function_to_execute()
        except ValueError:
            print("\n")
            print("A escolha tem que ser um número inteiro entre 1 e 4 inclusive.")

def list_files():
    recv_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    recv_socket.bind(('',10002))
    sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    message = {
        "type" : "LIST_FILES"
    }
    message = json.dumps(message).encode('utf8')
    sending_socket.sendto(message,('10.0.0.250', 10002))
    listing,address = recv_socket.recvfrom(20000)
    listing = json.loads(listing.decode('utf8'))
    files = listing["files"]
    print('----- Lista de ficheiros -----\n')
    i = 1
    for file in files:
        print(str(i) + ' - ' + file)
        i += 1

def file_upload():
    sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    file_path = raw_input("Insira o caminho do ficheiro que pretende enviar para o servidor")
    if os.path.isfile(file_path):
        file = open(file_path,"r")
        content = file.read()
        file_path_parts = file_path.split('/')
        file_name = file_path_parts[len(file_path_parts) - 1]
        message = {
            "type" : "FILE_UPLOAD",
            "file_name" : file_name,
            "content" : content
        }
        message = json.dumps(message).encode('utf8')
        sending_socket.sendto(message,('10.0.0.250',10003))
    else:
        print(' O caminho inserido não aponta para um ficheiro!')

def file_request():
    sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    file_name = raw_input("Insira o nome do ficheiro que pretende transferir: ")
    message = {
        "type" : "FILE_REQUEST",
        "file_name" : file_name
    }
    message = json.dumps(message).encode('utf8')
    sending_socket.sendto(message,('10.0.0.250', 10002))
    recv_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    recv_socket.bind(('',10002))
    file,address = recv_socket.recvfrom(100000)
    file = json.loads(file.decode('utf8'))
    if file["content"] == 'No file found!':
        print('O ficheiro não existe')
    else:
        local_file = open(file_name,'w')
        local_file.write(file["content"])
        local_file.close()
        print('O ficheiro ' + file_name + ' foi guardado com sucesso!')

def system_exit():
    sys.exit()

mainmenu()

