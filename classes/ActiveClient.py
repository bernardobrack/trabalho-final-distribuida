from typing import Dict, Union
from classes.process import Process, Process_type

class ActiveClient:
    def __init__(self, process_id, ip, port, replicas: Dict[int, Process_type], broadcast_sequencer: Union[Process_type, None], broadcastable):
        if(broadcast_sequencer == None):
            print("ERROR! An active client must know a broadcast sequencer")
            exit(-1)
        self.process = Process(process_id,ip,port,replicas,broadcast_sequencer)
    
    def replicate(self, m):
        self.process.broadcast({'m': m, 'client_id': self.process.id})
