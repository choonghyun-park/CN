import random
import socket
import json
from logHandler import *

class PASender:
    loss_rate = 0.0
    corrupt_rate = 0.0
    bit_error_rate = 0.1

    def __init__(self, soc, config_file=None, loss_rate=-1.0, corrupt_rate=-1.0, bit_error_rate=-1.0):
        self.soc = soc
        self.bit_error_rate = 0.1
        if config_file: # config.txt 에서 값을 가져오는 경우
            with open(config_file) as json_file:
                config_data = json.load(json_file)
                if "loss_rate" in config_data:
                    self.loss_rate = config_data["loss_rate"]
                if "corrupt_rate" in config_data:
                    self.corrupt_rate = config_data["corrupt_rate"]
                if "bit_error_rate" in config_data:
                    self.bit_error_rate = config_data["bit_error_rate"]
        else: # config.txt가 존재하지 않는 경우. 따로 매개변수를 넣어주지 않았으면 기본값을 사용한다.
            if 0 <= loss_rate <= 1:
                self.loss_rate = loss_rate
            if 0 <= corrupt_rate <= 1:
                self.corrupt_rate = corrupt_rate
            if 0 <= bit_error_rate <= 1:
                self.bit_error_rate = bit_error_rate

    def sendto(self, pkt_data, dst_addr):
        if 0 < self.loss_rate <= 1:
            if random.random() < self.loss_rate:
                return
        if 0 < self.corrupt_rate <= 1 and 0 < self.bit_error_rate <= 1:
            if random.random() < self.corrupt_rate:
                raw_data = pkt_data
                if type(pkt_data) is bytes:
                    raw_data = str(pkt_data, 'utf-8')
                elif type(pkt_data) is not str:
                    print("pkt_data of sendto() must be string or bytes!")
                raw_data = list(raw_data)
                iter_until = len(raw_data)
                for i in range(0, iter_until):
                    if random.random() < self.bit_error_rate:
                        tmp = ord(raw_data[i]) ^ int(random.random() * 256)
                        raw_data[i] = chr(tmp)
                pkt_data = bytes(''.join(raw_data), 'utf-8')
            if type(pkt_data) is str:
                pkt_data = bytes(''.join(pkt_data), 'utf-8')

        self.soc.sendto(pkt_data, dst_addr)

    def sendto_bytes(self, pkt_data, dst_addr):
        if type(pkt_data) is not bytes:
            print("pkt_data of sendto_bytes() must be bytes!")
        if 0 < self.loss_rate <= 1:
            if random.random() < self.loss_rate:
                return
        if 0 < self.corrupt_rate <= 1 and 0 < self.bit_error_rate <= 1:
            if random.random() < self.corrupt_rate:
                raw_data = list(pkt_data)
                iter_until = len(raw_data)
                for i in range(0, iter_until):
                    if random.random() < self.bit_error_rate:
                        raw_data[i] ^= int(random.random() * 256)
                pkt_data = bytes(raw_data)
        self.soc.sendto(pkt_data, dst_addr)


"""
# Usage
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender = PASender(sock, config_file="testfile.txt")
sender.sendto("packet_data", ("127.0.0.1", 10090)) 
# or sender.sendto_bytes("packet_data".encode(), ("127.0.0.1", 10090))
"""

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # sender socket

    sender = PASender(sock, config_file="config.txt") # sender class

    # test sending. 아래 두 함수의 결과가 동일함.
    # sender.sendto("packet_data", ("127.0.0.1", 10090)) 
    # sender.sendto_bytes("packet_data".encode(), ("127.0.0.1", 10090))
    
    test_file = "test_file.txt"
    BUFFER_SIZE = 1024
    PACKET_SIZE = BUFFER_SIZE-1 # packet_size는 최대 buffer_size-1 이다. 

    logger = logHandler()
    logger.startLogging("log_sender.txt")


    with open(test_file) as file:
        line = file.readline()
        SIZE = len(line)
        
        iterates = SIZE//PACKET_SIZE
        if SIZE%PACKET_SIZE!=0:
            iterates+=1
        
        for i in range(iterates):
            packet = line[i*PACKET_SIZE:(i+1)*PACKET_SIZE]
            assert len(packet)<BUFFER_SIZE
            # sender.sendto(packet, ("127.0.0.1", 10090)) # send to dst ("127.0.0.1", 10090)
            
            sender.sendto_bytes(packet.encode(), ("127.0.0.1", 10090))
            logger.writePkt(i,"Send DATA")

    logger.writeEnd()




    

