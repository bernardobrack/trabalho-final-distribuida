import sys
from classes.process import Process
from time import sleep

process0Dict = {
    'ip': "127.0.0.1",
    'port': 9032
    }

process1Dict = {
    'ip': "127.0.0.1",
    'port': 9033
    }

processes = {
    0: process0Dict,
    1: process1Dict
}

process0 = Process(0, process0Dict['ip'], process0Dict['port'], processes)
process1 = Process(1, process1Dict['ip'], process1Dict['port'], processes)
process0.send_message(1, "OI MEU DEUS")
process1.send_message(0, "AH, OI")
sleep(5)
print(process0.sent)
print(process1.sent)



