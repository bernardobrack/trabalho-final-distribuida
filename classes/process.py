import socket
import threading
from typing import List, Dict, Union
import json
from time import sleep


Process_type = Dict[str, Union[str, int]]

class Process:
    def __init__(self, process_id, ip, port, processes: Dict[int, Process_type], broadcast_sequencer: Union[None, Process_type] = None, broadcastable: Union[Dict[int, Process_type], None] = None):
        self.id = process_id
        self.ip = ip
        self.port = port
        self.processes: Dict[int, Dict[str, any]] = processes
        self.broadcast_sequencer_thread = None
        self.broadcast_sequencer = broadcast_sequencer
        if(broadcastable == None):
            self.broadcastable = self.processes
        else:
            self.broadcastable = broadcastable
        self.broadcast_socket = None
        self.deliv: List[int] = []
        self.sent: List[List[int]] = []
        self.sent_lock = threading.Lock()
        self.received = []
        self.to_deliver_queue = []
        self.to_deliver_broadcast_queue = []
        self.start_deliv_list()
        self.start_sent_list()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((ip, port))
            self.socket.listen(5)
        except:
            print("An error has ocurred and it was not possible to create a socket on the delivered ip:port address")
            exit(-1)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.start_sequencer()
        self.receive_thread.start()
    
    def start_sequencer(self):
        if(self.broadcast_sequencer == None):
            return
        try:
            ip = self.broadcast_sequencer['ip']
            port = self.broadcast_sequencer['port']
        except:
            print("Sequencer defined to none since no IP or PORT was given")
            self.broadcast_sequencer = None
            return
        try:
            self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.broadcast_socket.bind((ip, port))
            self.broadcast_socket.listen(5)
        except:
            return
        self.broadcast_sequencer_thread = threading.Thread(target=self.sequencer)
        self.broadcast_sequencer_thread.start()
        #print("CONTINUOU")
                
            
    def sequencer(self):
        #print("SEQUENCER")
        while True:
            try:
                conn, addr = self.broadcast_socket.accept()
            except:
                break
            data_s = conn.recv(2048).decode("UTF-8")
            data = json.loads(data_s)
            serialized = json.dumps({'sender_id': data['sender_id'], 'm': data['m'], 'sequencer': True})
            for processDict in self.broadcastable.values():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    host = processDict['ip']
                    port = processDict['port']
                    s.connect((host, port))
                    s.sendall(bytes(serialized, encoding="UTF-8"))



    def start_deliv_list(self) -> None:
        for i in self.processes:
            self.deliv.append(0)

    def start_sent_list(self) -> None:
        for i in (self.processes):
            row = []
            for j in (self.processes):
                row.append(0)
            self.sent.append(row)

    def send(self, target_id, message):
        host = self.processes[target_id]['ip']
        port = self.processes[target_id]['port']
        data = {
            'message': message,
            'sent': self.sent,
            'sender_id': self.id
        }
        self.sent_lock.acquire()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            serialized_d = json.dumps(data)
            s.sendall(bytes(serialized_d, encoding="UTF-8"))
        self.sent[self.id][target_id] += 1
        self.sent_lock.release()
    
    def delayed_send_thread(self, target_id, message):
        host = self.processes[target_id]['ip']
        port = self.processes[target_id]['port']
        sent = []
        for array in self.sent:
            sent.append(array.copy())
        data = {
            'message': message,
            'sent': sent,
            'sender_id': self.id
        }
        self.sent_lock.acquire()
        self.sent[self.id][target_id] += 1
        self.sent_lock.release()
        sleep(3)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            serialized_d = json.dumps(data)
            s.sendall(bytes(serialized_d, encoding="UTF-8"))

    def delayed_send(self, target_id, message):
        t = threading.Thread(target=self.delayed_send_thread, args=[target_id, message])
        t.start()

    def receive_message(self, sender_id, message, st):
        #print(f"Process {self.id} received message from {sender_id} with SENT {st}: {message}")
        deliverable = True
        for k, v in enumerate(self.deliv):
            if(st[k][self.id] > v ):
                deliverable = False
        if(not deliverable):
            self.received.append((sender_id,message,st))
            return
        # Pode dar deliver
        self.received.append((sender_id, message, st))
        self.deliver_message(sender_id, message, st)
        self.deliv[sender_id] =+ 1
        self.sent[sender_id][self.id] += 1
        for k in range(len(self.sent)):
            for l in range(len(self.sent)):
                self.sent[k][l] = max(self.sent[k][l], st[k][l])
        
        self.check_for_deliverable()
    
    def check_for_deliverable(self):
        any_delivered = False
        for sender_id, message, st in self.received:
            deliverable = True
            for k, v in enumerate(self.deliv):
                if(st[k][self.id] > v ):
                  deliverable = False
            if(deliverable):
                any_delivered = True
                self.deliver_message(sender_id,message,st)
                self.deliv[sender_id] =+ 1
                self.sent[sender_id][self.id] += 1
                for k in range(len(self.sent)):
                    for l in range(len(self.sent)):
                        self.sent[k][l] = max(self.sent[k][l], st[k][l])
        if(any_delivered):
            self.check_for_deliverable()

    def deliver_message(self, sender_id, message, st):
        self.to_deliver_queue.append(message)
        self.received.remove((sender_id, message, st))
    
    def receive(self):
        while(len(self.to_deliver_queue) <= 0):
            continue
        return self.to_deliver_queue.pop(0)
    
    def receive_messages(self):
        while True:
            try:
                conn, addr = self.socket.accept()
            except:
                break
            data_s = conn.recv(2048).decode("UTF-8")
            data = json.loads(data_s)
            if data:
                sequencer = data.get('sequencer', False)
                if(sequencer):
                    # Broadcast receive
                    self.to_deliver_broadcast_queue.append(data['m'])
                    continue
                self.sent_lock.acquire()
                self.receive_message(data['sender_id'], data['message'], data['sent'])
            self.sent_lock.release()
            conn.close()
    
    def broadcast(self,m):
        if(self.broadcast_sequencer == None):
            print("You are not allowed to broadcast since no sequencer IP:PORT was given")
            return
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.broadcast_sequencer['ip'], self.broadcast_sequencer['port']))
                serialized_d = json.dumps({'m': m, 'sender_id': self.id})
                s.sendall(bytes(serialized_d, encoding="UTF-8"))
        except:
            print('An error ocurred when sending broadcast message to sequencer')
    
    def deliver(self):
        while(len(self.to_deliver_broadcast_queue) <= 0):
            continue
        return self.to_deliver_broadcast_queue.pop(0)
    
    def end(self):
        self.socket.close()
        self.socket = None
        if(self.broadcast_socket != None):
            self.broadcast_socket.close()
            self.broadcast_socket = None

    def isAlive(self):
        return self.socket != None