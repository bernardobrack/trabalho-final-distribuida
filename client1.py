import sys
from classes.process import Process

processes = {
    0: {
        'ip': '127.0.0.1',
        'port': 9034
    },
    1: {
        'ip': '127.0.0.1',
        'port': 9035
    },
    2: {
        'ip': '127.0.0.1',
        'port': 9036
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
cliente.send(0, "MENSAGEM DE 4")
cliente.receive()
cliente.end()