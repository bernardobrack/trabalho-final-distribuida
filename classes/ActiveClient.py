from typing import Dict, Union
from classes.process import Process, Process_type

class ActiveClient:
    def __init__(self, process_id, ip, port, replicas: Dict[int, Process_type], broadcast_sequencer: Union[Process_type, None], broadcastable: Dict[int, Process_type]):
        if(broadcast_sequencer == None):
            print("ERROR! An active client must know a broadcast sequencer")
            exit(-1)
        self.counter: int = 0
        self.process = Process(process_id,ip,port,replicas,broadcast_sequencer, broadcastable)
    
    def replicate(self, m):
        self.process.broadcast({'m': m, 'client_id': self.process.id})

    def receive(self):
        message = self.process.receive()
        while(message.get('counter') <= self.counter):
            message = self.process.receive()
        self.counter = message.get('counter')
        return message.get('m')
    
    def end(self):
        self.process.end()

