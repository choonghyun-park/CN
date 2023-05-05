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

def cal_checksum(data):
    if data=='finish':
        return 0
    checksum = int(data,16) # 8bit str
    checksum = ~checksum
    # bin_data_str = ''.join(format(ord(i), '08b') for i in data)  # 문자열을 이진(binary)으로 변환
    # bin_data = int(bin_data_str,2)
    # checksum = ~bin_data
    # checksum = '{0:b}'.format(checksum).zfill(32) # 32 자리로 맞추기. 남는자리에 0을 넣어줌.
    
    return checksum

def cal_checksum2(data1,data2):
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
    '''
    checksum : 16-bit(=2B) 보수 계산
    buffer_size = 1024B
    data_size = bf/4 = 256B




    
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # sender socket

    sender = PASender(sock, config_file="config.txt") # sender class

    # test sending. 아래 두 함수의 결과가 동일함.
    # sender.sendto("packet_data", ("127.0.0.1", 10090)) 
    # sender.sendto_bytes("packet_data".encode(), ("127.0.0.1", 10090))
    
    test_file = "test_file.txt"
    BUFFER_SIZE = 2 * 1024 # 1KB = 1024B = 1024 * 8bit
    DATA_SIZE = BUFFER_SIZE//4 # 그냥 정했음.
    # DATA_SIZE = int(BUFFER_SIZE/2-1) # packet_size는 최대 buffer_size-1 이다. 안전하게 (buffer의 절반 -1) 크기로 보낸다.

    logger = logHandler()
    logger.startLogging("log_sender.txt")

    seq = 0

    with open(test_file) as file:

        '''
        udp segment
        header
            - source port
            - dest port
            - length
            - checksum
        body
            - data

        * 보내는 msg에 header와 body 파트로 나눠서 보내기로 했다. 
        * length는 일단 필요없어서 안만들었다. 가변성이 너무 크기도 하고..
        * checksum은 일단, 데이터 하나 기준으로 계산한다. 즉, 보수만 취하고 남는 자리에 0을 채워서 보낸다.
        * ack은 다음 받아야 할 seq가 아니라, seq를 그대로 다시 응답으로 실어서 보내준다.
        '''
        
        line = file.readline()
        datas = []
        FILE_SIZE = len(line)

        iterates = FILE_SIZE//DATA_SIZE
        if FILE_SIZE%DATA_SIZE!=0:
            iterates+=1
        
        for i in range(iterates):
            data = line[i*DATA_SIZE:(i+1)*DATA_SIZE] # 4B
            datas.append(data)
        datas.append("finish")

        # checksum을 반드시 모든 데이터에 대해서 수행할 필요는 없어보인다.
        # seq의 주기를 따르는 것이 옳다고 본다.
        seqs = (0,1)
        checksum = None
        for i,data in enumerate(datas):
            if i%10==0:
                print("Sending [{}/{}] data...".format(i+1,len(datas)))
            # packet 만들기
            seq = seqs[i%2] # 0,1 을 번갈아가며 보내주기.
            checksum = cal_checksum(data) 
            packet = make_msg(data,seq,checksum)

            send_flag = True     
            resend_flag = False       

            # Receive Response
            while True:
                if send_flag or resend_flag:
                    sender.sendto(packet, ("127.0.0.1", 10090)) # send to dst ("127.0.0.1", 10090)
                    # sender.sendto_bytes(packet.encode(), ("127.0.0.1", 10090))
                    if send_flag:
                        logger.writePkt(i,"Send DATA")
                        send_flag = False
                    elif resend_flag:
                        logger.writePkt(i,"Send DATA Again")
                        resend_flag = False

                sock.settimeout(1)
                try:
                    response, addr = sock.recvfrom(1024)
                except socket.timeout:  
                    logger.writeTimeout(seq)
                    # print("Timeout!!")
                    resend_flag = True
                    continue
                except OSError:
                    print("Buffer overflow!!")
                    continue

                decode_response = response.decode()
                split_data = decode_response.split()

                # extract ack
                ack = int(split_data[1])
                if ack==seqs[i%2]:
                    logger.writePkt(i,"Sent Successfully")
                    break
                else:
                    logger.writePkt(i,"Wrong Sequence Number")
                    resend_flag=True

    logger.writeEnd()

