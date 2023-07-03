from classes.process import Process, Process_type
from typing import Dict, Union
from threading import Lock

class Replicate:
    def __init__(self, id, ip, port, processes: Dict[int, Process_type], broadcast_sequencer: Union[None, Process_type]) -> None:
        if(processes[id]['type'] != 'r'):
            print("A Replica process must have 'type': 'r' in it's Dict")
            exit(-1)
        self.process = Process(id, ip, port, processes, broadcast_sequencer)
        self.processes = processes
        self.id = id

    def _dealWithMessage(self, m):
        pass

    def _replicate(self):
        pass

    def end(self):
        self.process.end()

class PassiveReplica(Replicate):

    def __init__(self, id, ip, port, processes: Dict[int, Process_type]) -> None:
        super().__init__(id, ip, port, processes, None)
        self._run()

    def _replicate(self, m):
        for id in self.processes.keys():
            if('type' in self.processes[id]):
                if(self.id != id and self.processes[id]['type'] == 'r'):
                    self.process.send(id, {'m': m, 'replica_id': self.id})

    def _run(self):
        while(self.process.isAlive()):
            message = self.process.receive()
            sender_id = None
            try:
                sender_id = message['replica_id']
            except:
                if(sender_id == None):
                    # From client
                    self._replicate(message)
            else:
                # From another replica
                message = message['m']
            finally:
                self._dealWithMessage(message)
    
    def _dealWithMessage(self, message):
        print(message)

class ActiveReplica(Replicate):
    def __init__(self, id, ip, port, processes, broadcast_sequencer) -> None:
        super().__init__(id, ip, port, processes, broadcast_sequencer)
        self.kvStorage: Dict[str, any] = {}
        self.messageCounter: int = 1
        self._run()
    
    def _run(self):
        while(self.process.isAlive()):
            data = self.process.deliver()
            message = data['m']
            client_id = data['client_id']
            self._dealWithMessage(message, client_id)

    def _dealWithMessage(self, message, client_id):
        if(message.get('operation') == 'put'):
            self.kvStorage['key'] = message.get('value')
            print(f"Value of key {message.get('key')} updated to {message.get('value')}")
        if(message.get('operation') == 'get'):
            self.process.send(client_id, {'m': self.kvStorage.get('key'), 'counter': self.messageCounter})
            self.messageCounter += 1
        if(message.get('operation') == 'show'):
            print(self.kvStorage)