import sys
sys.path.append('..')
from classes.replicate import PassiveReplica

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

replica = PassiveReplica(2, processes[2]['ip'], processes[2]['port'], processes)