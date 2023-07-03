import sys
sys.path.append('..')
from classes.process import Process
from time import sleep

processes = {
    0: {
        'ip': '127.0.0.1',
        'port': 9034,
        'type': 'r'
    },
    1: {
        'ip': '127.0.0.1',
        'port': 9035,
        'type': 'r'
    },
    2: {
        'ip': '127.0.0.1',
        'port': 9036,
        'type': 'r'
    },
    3: {
        'ip': '127.0.0.1',
        'port': 9037
    },
    4: {
        'ip': '127.0.0.1',
        'port': 9038
    }
}

cliente = Process(4, processes[4]['ip'],processes[4]['port'], processes, None)
cliente.send(1, "MENSAGEM 1 DE 1")
cliente.send(1, "MENSAGEM 2 DE 1")
sleep(1)
cliente.send(2, "MENSAGEM 3 DE 1")
cliente.end()