import socket

# 통신 정보 설정
IP = '127.0.0.1'
PORT = 10090
SIZE = 1024
ADDR = (IP, PORT)

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
        print(decode_data)
        # print("Sender IP",addr[0])
        # print("Sender Port",addr[1])
    
