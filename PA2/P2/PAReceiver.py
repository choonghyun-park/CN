import socket
import json
from logHandler import *

# 통신 정보 설정
IP = '127.0.0.1'
PORT = 10090
# SIZE = 1024
SIZE = 2 * 1024
ADDR = (IP, PORT)


def cal_checksum(data):
    if data=='finish':
        return 0
    checksum = int(data,16) # 8bit str
    checksum = ~checksum
    # bin_data_str = ''.join(format(ord(i), '08b') for i in data)  # 문자열을 이진(binary)으로 변환.
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

def make_msg(ack):
    # make empty body
    body = {}
    body = json.dumps(body)

    # make header
    headers = []
    headers.append('ack: {}'.format(ack))
    header = ''
    for h in headers:
        header += h
        header += '\r\n'
    header += '\r\n'

    msg = header + body
    msg = bytes(msg, encoding='utf-8')
    
    return msg


if __name__=='__main__':
    expected_seq = 0
    other_seq = (1,0)
    datas = []
    logger = logHandler()
    logger.startLogging("log_receiver.txt")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(ADDR) # 서버의 port, ip 주소 지정
        
        while True:
            server_socket.settimeout(1)
            try:
                data, addr = server_socket.recvfrom(SIZE)
            except socket.timeout:
                continue
            except OSError:
                print("Buffer overflow!!")
                continue

            decode_data = data.decode()
            split_data = decode_data.split('\r\n')

            # extract data
            try:
                seq = int(split_data[0].split()[1]) # 기본적으로 str이다. int로 변환해줘야함.
                checksum = split_data[1].split()[1] # checksum은 str인 상태로 비교함.
                body = split_data[-1]
                body = json.loads(body)
                data = body["data"]
                cal_cs = str(cal_checksum(data))
            except:
                # Any Error occured in transmission : send NAK
                packet = make_msg(other_seq[expected_seq])
                server_socket.sendto(packet, addr)
                logger.writeAck(seq,"DATA Corrupted")
                continue

            # check seq and checksum
            if seq==expected_seq and checksum==cal_cs:
                expected_seq = other_seq[expected_seq]
                packet = make_msg(seq) # 받은 seq를 ACK으로 보내줌.
                logger.writeAck(seq,"Send ACK")
            else:
                # Send NAK
                packet = make_msg(other_seq[expected_seq])
                logger.writeAck(other_seq[expected_seq],"Send ACK Again")

            # collect data
            if data!="finish":
                # 응답
                datas.append(data)
                server_socket.sendto(packet, addr)
                idx = len(datas)
                if idx%10==1:
                    print("Sending {}th ACK...".format(idx))
            else:
                server_socket.sendto(packet, addr)
                break

        logger.writeEnd()
