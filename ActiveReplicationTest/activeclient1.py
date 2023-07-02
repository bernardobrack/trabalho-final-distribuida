import sys
sys.path.append('..')
from classes.ActiveClient import ActiveClient


replicas = {
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
    }
}

replicas_and_self = {
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
    4: {
        'ip': '127.0.0.1',
        'port': 9038
    }
}

broadcast_sequencer = {
    'ip': '127.0.0.1',
    'port': 9039
}

cliente = ActiveClient(4, replicas_and_self[4]['ip'], replicas_and_self[4]['port'], replicas_and_self, broadcast_sequencer, replicas)
cliente.replicate('REPLICANDO 5')
cliente.replicate('REPLICANDO 6')
cliente.replicate('REPLICANDO 7')
cliente.replicate('REPLICANDO 8')
cliente.replicate('REPLICANDO 9')