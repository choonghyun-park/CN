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
        if config_file:
            with open(config_file) as json_file:
                config_data = json.load(json_file)
                if "loss_rate" in config_data:
                    self.loss_rate = config_data["loss_rate"]
                if "corrupt_rate" in config_data:
                    self.corrupt_rate = config_data["corrupt_rate"]
                if "bit_error_rate" in config_data:
                    self.bit_error_rate = config_data["bit_error_rate"]
        else:
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

def cal_checksum(data1,data2):
    if data2 is None:
        bin_data1 = ''.join(format(ord(i), '08b') for i in data1)  # 문자열을 이진(binary)으로 변환
        bin_data1 = '0b'+bin_data1
        checksum = ~bin_data1
        checksum = '{0:b}'.format(checksum).zfill(32) # 32 자리로 맞추기. 남는자리에 0을 넣어줌.
        
        return checksum

    # 초기 data1, data2는 4B(=32bit) str이다. 이를 2진수의 binary string으로 바꿔준다.
    bin_data1 = ''.join(format(ord(i), '08b') for i in data1)  # 문자열을 이진(binary)으로 변환
    bin_data2 = ''.join(format(ord(i), '08b') for i in data2)  # 문자열을 이진(binary)으로 변환

    # binary 2개를 서로 더해주기
    checksum = int(bin_data1,2) + int(bin_data2,2)
    # checksum = bin_data1+bin_data2

    # 자리 넘김이 있는지 확인
    if checksum >= pow(2,32):
        added = checksum//pow(2,32)
        checksum = checksum%pow(2,32)       # 자리넘김 부분 없애기
        checksum += added                   # 1의 자리에 더해주기
        checksum = bin(checksum)            # 10진수 -> 2진수
        checksum = ~checksum                # 보수
        checksum = checksum[2:]             # 앞에 0b(?) 이거 없애주기.
        checksum = '{0:b}'.format(checksum).zfill(32) # 32 자리로 맞추기. 남는자리에 0을 넣어줌.
    return checksum

def make_msg(data,seq,checksum):
    # make body
    body = {"data":data}
    body = json.dumps(body)
    # length = len(body) # body와 header를 합쳐서 계산해야 하는데, 이게 까다로움

    # make header
    headers = []
    # headers.append('length: {}'.format(length))
    headers.append('seq: {}'.format(seq))
    headers.append('checksum: {}'.format(checksum))
    header = ''
    for h in headers:
        header += h
        header += '\r\n'
    header += '\r\n'

    msg = header + body
    msg = bytes(msg, encoding='utf-8')
    
    return msg


if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # sender socket

    sender = PASender(sock, config_file="config.txt") # sender class

    # test sending. 아래 두 함수의 결과가 동일함.
    # sender.sendto("packet_data", ("127.0.0.1", 10090)) 
    # sender.sendto_bytes("packet_data".encode(), ("127.0.0.1", 10090))
    
    test_file = "test_file.txt"
    BUFFER_SIZE = 1024 # 1KB = 1024B = 1024 * 8bit
    DATA_SIZE = 4 # 4B 로 그냥 정했음.
    # DATA_SIZE = int(BUFFER_SIZE/2-1) # packet_size는 최대 buffer_size-1 이다. 안전하게 (buffer의 절반 -1) 크기로 보낸다.

    logger = logHandler()
    logger.startLogging("log_sender.txt")

    seq = 0

    with open(test_file) as file:
        line = file.readline()

        '''
        udp segment
        header
            - source port
            - dest port
            - length
            - checksum
        body
            - data

        여기서 ACK(seq)만 있으면 필요한 건 다 들어간 거임. ACK은 TCP segment에 존재하는 것인데, UDP의 Body와 header 중 어디에 넣어야 할지 좀 애매하긴 하다.
        넣는다면 header가 맞긴 할듯. 

        
        [client]
        data, addr = server_socket.recvfrom(SIZE)
        '''    

        
        '''
        전체 데이터를 나눠서 보낼껀데, 데이터 크기를 얼마로 잡을지가 문제이다.
        [고려사항]
        header 크기
        buffer size : buffer size보다 1만큼 작게만 보내면 되는 줄 알았는데, 가끔 버퍼 오버플로우가 발생한다. 
                    원인이 명확하지 않다. 아마 header의 크기가 조금이라도 생겨서 그럴 것 같기는 하다.

        
        '''
        
        datas = []
        SIZE = len(line)

        iterates = SIZE//DATA_SIZE
        if SIZE%DATA_SIZE!=0:
            iterates+=1
        
        for i in range(iterates):
            data = line[i*DATA_SIZE:(i+1)*DATA_SIZE] # 4B
            datas.append(data)


        # checksum을 반드시 모든 데이터에 대해서 수행할 필요는 없어보인다.
        # seq의 주기를 따르는 것이 옳다고 본다.
        seqs = (0,1)
        checksum = None
        for i,data in enumerate(datas):
            # 0,1 을 번갈아가며 보내주기.
            seq = seqs[i%2]
            
            if i%2==0:
                # 짝수 idx + 마지막 자리 
                if i==len(datas)-1:
                    checksum = cal_checksum(datas[i],None)
                else:
                    checksum = cal_checksum(datas[i],datas[i+1])

            # checksum 기록
            packet = make_msg(data,seq,checksum)
            
            sender.sendto(packet, ("127.0.0.1", 10090)) # send to dst ("127.0.0.1", 10090)
            print(packet)
            print()
            # sender.sendto_bytes(packet.encode(), ("127.0.0.1", 10090))
            logger.writePkt(i,"Send DATA")

    logger.writeEnd()

