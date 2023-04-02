#-*- coding:utf-8 -*-

import socket
import json

# 통신 정보 설정
IP = ''
PORT = 1398
SIZE = 1024
ADDR = (IP, PORT)


# 서버 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)  # 주소 바인딩
    server_socket.listen()  # 클라이언트의 요청을 받을 준비
    
    while True:
        server_socket.settimeout(1)
        try:
            client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
        except socket.timeout:
            continue
        server_socket.settimeout(None)
        msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
        
        # msg & decode
        decode_msg = msg.decode()
        print("========= decode_msg ==========")
        print(decode_msg)
        # print(decode_msg[0])              # G
        # print(type(decode_msg))           # str
        # print(decode_msg.split()) 
        # print(type(decode_msg.split()))   # list

        ''' decode_msg.split()
        ['GET', '/hi', 'HTTP/1.1', 
        'Host:', 'localhost:1398', 
        'Connection:', 'keep-alive', 
        'sec-ch-ua:', '"Google', 'Chrome";v="111",', '"Not(A:Brand";v="8",', '"Chromium";v="111"', 
        'sec-ch-ua-mobile:', '?0', 
        'User-Agent:', 'Mozilla/5.0', '(Windows', 'NT', '10.0;', 'Win64;', 'x64)', 'AppleWebKit/537.36', '(KHTML,', 'like', 'Gecko)', 
        'Chrome/111.0.0.0', 'Safari/537.36', 
        'sec-ch-ua-platform:', '"Windows"', 
        'Accept:', '*/*', 
        'Origin:', 'http://127.0.0.1:5500', 
        'Sec-Fetch-Site:', 'cross-site', 
        'Sec-Fetch-Mode:', 'cors', 'Sec-Fetch-Dest:', 
        'empty', 'Referer:', 'http://127.0.0.1:5500/', 
        'Accept-Encoding:', 'gzip,', 'deflate,', 'br', 
        'Accept-Language:', 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7']
        '''
        

        # print(client_addr)    # client address ('127.0.0.1', 54029)
        # print(msg)            # raw message

        # 클라이언트에게 응답
        client_socket.sendall("welcome!".encode())

        # 클라이언트 소켓 종료  
        client_socket.close()  
