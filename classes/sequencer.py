from typing import List;
import socket

class Sequencer:
    def __init__(self, info) -> None:
        self.seq_num = 1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((info['ip'], info['port']))
        self.socket.listen(5)
        