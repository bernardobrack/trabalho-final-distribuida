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
    3: {
        'ip': '127.0.0.1',
        'port': 9037
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

cliente = ActiveClient(3, replicas_and_self[3]['ip'], replicas_and_self[3]['port'], replicas_and_self, broadcast_sequencer, replicas)
while(True):
    op = str(input('Operation (put, get, show, q)'))
    if(op == 'q'):
        break
    key = str(input('Key: '))
    value = str(input('value: '))
    cliente.replicate({
        'operation': op,
        'key': key,
        'value': value
    })
    if(op == 'get'):
        cliente.receive()
cliente.end()