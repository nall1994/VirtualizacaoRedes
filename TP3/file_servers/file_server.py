# coding=utf-8

import socket
import json
import psutil
from time import sleep
from threading import Thread


class FileServer:

    def __init__(self):
        self.known_files = dict() # Dicionário que mapeia nome_ficheiro -> path para o ficheiro (no servidor)
        self.known_files["ex1"] = "filesystem/ex1.txt"
        self.known_files["ex2"] = "filesystem/ex2.txt"
        self.server_load = 0.0 # métrica que faz uma média entre cpu e ram utilizada. 50% de interesse para cada valor.

    def listen_request(self):
        recv_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        recv_socket.bind(('',10002))
        sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        while True:
            message, address = recv_socket.recvfrom(4096)
            message = json.loads(message.decode('utf8'))
            if message["type"] == "LIST_FILES":
                files_list = self.list_known_files()
                sending_socket.sendto(files_list,(address[0],10002))
            elif message["type"] == "FILE_REQUEST":
                file_name = message["file_name"]
                file_to_send = self.file_request(file_name)
                sending_socket.sendto(file_to_send,(address[0],10002))

    def list_known_files(self):
        files_array = []
        for kf in self.known_files:
            files_array.append(kf)
        info_to_return = {
            "files": files_array
        }
        info_to_return = json.dumps(info_to_return).encode('utf8')
        return info_to_return

    def file_request(self,file_name):
        file_path = self.known_files[file_name]
        info_to_return = {
            "content": "No file found!"
        }
        if file_path == None:
            return info_to_return
        else:
            file = open(file_path,"r")
            file_content = file.read()
            info_to_return["content"] = file_content
            info_to_return = json.dumps(info_to_return).encode('utf8')
        return info_to_return
    
    def uploads_listener(self):
        recv_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        recv_socket.bind(('',10003))
        while True:
            message, address = recv_socket.recvfrom(100000)
            message = json.loads(message.decode('utf8'))
            if message["type"] == "FILE_UPLOAD":
                file_name = message["file_name"]
                file_content = message["content"]
                file_path = 'filesystem/' + file_name
                self.known_files[file_name] = file_path
                file_to_write = open(file_path, 'w')
                file_to_write.write(file_content)

    
    def calculate_server_load(self):
        cpu_percent = psutil.cpu_percent()
        ram_stats = psutil.virtual_memory()
        ram_percent = ram_stats[2]
        server_load = cpu_percent * 0.5 + ram_percent * 0.5
        return server_load

    def send_load_updates(self):
        while True:
            sleep(5)
            server_load = self.calculate_server_load()
            sending_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
            sending_socket.sendto(str(server_load),('10.0.0.50',10001))
            
file_server = FileServer()
server_load_thread = Thread(target=file_server.send_load_updates)
requests_thread = Thread(target=file_server.listen_request)
uploads_thread = Thread(target=file_server.uploads_listener)
server_load_thread.start()
requests_thread.start()
uploads_thread.start()
