import sys

sys.path.append('..')


from classes.replicate import ActiveReplica


allProcesses = {
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

broadcast_sequencer = {
    'ip': '127.0.0.1',
    'port': 9039
}


replica = ActiveReplica(2,allProcesses[2]['ip'], allProcesses[2]['port'], allProcesses, broadcast_sequencer, replicas)