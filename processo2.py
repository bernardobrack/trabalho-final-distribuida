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
process2Dict = {
    'ip': "127.0.0.1",
    'port': 9034
}

processes = {
    0: process0Dict,
    1: process1Dict,
    2: process2Dict
}    
try:
    process_id = int(sys.argv[1])
except:
    print("ERROR! You must inform de id of the process")
    exit(-1) 
    
process = Process(process_id, processes[process_id]['ip'], processes[process_id]['port'], processes)

sleep(10)
process.send_message(0, "OLÁ")
process.send_message(0, "AHAHAH")
