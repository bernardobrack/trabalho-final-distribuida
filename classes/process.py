import socket
import threading
from typing import List
import json

class Process:
    def __init__(self, process_id, ip, port, processes):
        self.id = process_id
        self.ip = ip
        self.port = port
        self.processes = processes
        self.deliv: List[int] = []
        self.sent: List[List[int]] = []
        self.start_deliv_list()
        self.start_sent_list()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(1)
        
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
    
    def start_deliv_list(self) -> None:
        for i in self.processes:
            self.deliv.append(0)

    def start_sent_list(self) -> None:
        for i in (self.processes):
            row = []
            for j in (self.processes):
                row.append(0)
            self.sent.append(row)

    def send_message(self, target_id, message):
        host = self.processes[target_id]['ip']
        port = self.processes[target_id]['port']
        data = {
            'message': message,
            'sent': self.sent,
            'sender_id': self.id
        }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            serialized_d = json.dumps(data)
            print(serialized_d)
            s.sendall(bytes(serialized_d, encoding="UTF-8"))
        self.sent[self.id][target_id] += 1

    def receive_message(self, sender_id, message, st):
        print(f"Process {self.id} received message from {sender_id} with SENT {st}: {message}")
        do_not_deliver = True
        while(do_not_deliver):
            do_not_deliver = False
            for k, v in enumerate(self.deliv):
                if(st[k][self.id] > v ):
                    do_not_deliver = True
        self.deliver_message(message)
        self.deliv[sender_id] =+ 1
        self.sent[sender_id][self.id] += 1

        for k in range(len(self.sent)):
            for l in range(len(self.sent)):
                self.sent[k][l] = max(self.sent[k][l], st[k][l])

    def deliver_message(self, message):
        print("DELIVERED: ", message)
    
    def receive_messages(self):
        while True:
            conn, addr = self.socket.accept()
            data_s = conn.recv(2048).decode("UTF-8")
            print(data_s)
            data = json.loads(data_s)
            if data:
                self.receive_message(data['sender_id'], data['message'], data['sent'])
            conn.close()