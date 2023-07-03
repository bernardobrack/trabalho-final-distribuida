import sys
sys.path.append('..')
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

cliente = Process(3, processes[3]['ip'],processes[3]['port'], processes, None)
cliente.send(0, "MENSAGEM 1 DE 0")
cliente.send(0, "MENSAGEM 2 DE 0")
cliente.end()