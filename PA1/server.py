#-*- coding:utf-8 -*-

import socket
import json

# 통신 정보 설정
IP = ''
PORT = 1398
SIZE = 1024
ADDR = (IP, PORT)

users = {}

def get_hi(client_socket):
    response = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 16\r\nAccess-Control-Allow-Origin: *\r\n\r\n{"message":"hi"}'
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def post_echo(client_socket,msg_body_dict):
    try:
        m = msg_body_dict["message"]
    except:
        m = None
    
    # make body
    body = {"message":m}
    body = json.dumps(body)
    leng = len(body)

    # make header
    headers = []
    headers.append('HTTP/1.1 200 OK')
    headers.append('Content-Type: application/json')
    headers.append('Content-Length: {}'.format(leng))
    headers.append('Access-Control-Allow-Origin: *')
    header = ''
    for h in headers:
        header += h
        header += '\r\n'
    header += '\r\n'

    response = header + body
    response = bytes(response, encoding='utf-8')
    
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def post_user(client_socket,msg_body_dict):
    try:
        id = msg_body_dict["id"]
        name = msg_body_dict["name"]
        gender = msg_body_dict["gender"]
    except KeyError:
        # 400
        response = b'HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        # response = b'HTTP/1.1 400 Bad Request\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        client_socket.send(response)
        print("========= sent_msg   ==========")
        print(response)
        return
    # id가 존재하지 않는 경우등록
    if id not in users.keys():
        users[id]=(name,gender)
        # 201
        response = b'HTTP/1.1 201 Created\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        # response = b'HTTP/1.1 201 Created\r\nAccess-Control-Allow-Origin: *\r\n\r\n'

    # 기존에 등록된 id : 409
    else:
        response = b'HTTP/1.1 409 Registered id\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        # response = b'HTTP/1.1 409 Registered id\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def get_user(client_socket,query):
    id = query[1]
    assert id in users.keys()
    
    user_info = users[id]
    name = user_info[0]
    gender = user_info[1]

    # make body
    body = {"id":id,"name":name,"gender":gender}
    body = json.dumps(body)
    leng = len(body)

    # make header
    headers = []
    headers.append('HTTP/1.1 200 OK')
    headers.append('Content-Type: application/json')
    headers.append('Content-Length: {}'.format(leng))
    headers.append('Access-Control-Allow-Origin: *')
    header = ''
    for h in headers:
        header += h
        header += '\r\n'
    header += '\r\n'

    response = header + body
    response = bytes(response, encoding='utf-8')
    
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def options_user(client_socket):
    # make header
    headers = []
    headers.append('HTTP/1.1 200 OK')
    # headers.append('Connection: keep-alive')
    headers.append('Access-Control-Allow-Origin: *')
    headers.append('Access-Control-Allow-Headers: *')
    headers.append('Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE, PUT')
    headers.append('Access-Control-Max-Age: 86400')
    header = ''
    for h in headers:
        header += h
        header += '\r\n'
    header += '\r\n'

    # make body
    body = ''

    response = header + body
    response = bytes(response, encoding='utf-8')

    # single response
    # response = b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\nAccess-Control-Request-Headers: *\r\n\r\n'
    
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def delete_user(client_socket,user_id):
    del(users[user_id])
    response = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n\r\n'
    
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

def put_user(client_socket,msg_body_dict,user_id):
    id = user_id
    try:
        name = msg_body_dict["name"]
    except KeyError:
        # 400, 요청 무시
        response = b'HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        client_socket.send(response)
        return
    if "id" in msg_body_dict.keys() or "gender" in msg_body_dict.keys():
        # 400, 요청 무시
        response = b'HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
        client_socket.send(response)
        return
    user_info = users[id]
    if name==user_info[0]:
        # 기존에 등록된 name과 동일 : 요청 무시, 422
        response = b'HTTP/1.1 422 Unprocessable Entity\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
    else:
        # 수정 진행
        new_user_info = (name,user_info[1])
        users[id]=new_user_info
        # 200
        response = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n\r\n'
    client_socket.send(response)

def page_not_found(client_socket):
    response = b'HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n\r\n'

    client_socket.send(response)

def null_response(client_socket):
    response = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 0\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
    
    client_socket.send(response)
    print("========= sent_msg   ==========")
    print(response)

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
        # print(client_addr)                # ('127.0.0.1', 54029)
        print("===============================")
        print("========= raw_msg    ==========")
        print(msg)                        # raw message : binary
        if msg==b'': 
            print("message length is too small. So, ignored.")
            continue
        
        # msg & decode
        decode_msg = msg.decode()
        print("========= decode_msg ==========")
        print(decode_msg)
        # print(decode_msg[0])              # G
        # print(type(decode_msg))           # str
        # print(decode_msg.split()) 
        # print(type(decode_msg.split()))   # list

        '''Q1 : decode_msg.split() 
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
        
        # client info
        split_msg = decode_msg.split()
        
        method = split_msg[0]
        parmalink = split_msg[1]
        host = split_msg[4]
        msg_body = split_msg[-1]        # if data exists, get 'json string', type : str
        try:
            msg_body_dict = json.loads(msg_body)
        except:
            msg_body_dict = {}

        # find query values
        split_query = parmalink.split('?')
        if len(split_query)>1:
            parmalink = split_query[0]
            query = split_query[1].split('=') # ["id","chp"]
        
        user_id = parmalink.split('/')

        if len(user_id)>2:
            if user_id[-1] in users.keys():
                parmalink = '/' + user_id[1]
                user_id = user_id[-1]
            else:
                user_id = None
        
        # Preflight은 무조건 응답
        if method=='OPTIONS':
            options_user(client_socket)
            continue

        parmalinks = {'/hi','/echo','/user'}
        if parmalink not in parmalinks: 
            page_not_found(client_socket)

        if parmalink=='/hi' and method=='GET':
            get_hi(client_socket)
        elif parmalink=='/echo' and method=='POST':
            post_echo(client_socket,msg_body_dict)        
        elif parmalink=='/user' and method=='POST':
            post_user(client_socket,msg_body_dict)
        elif parmalink=='/user' and method=='GET':
            if query[1] not in users.keys():
                page_not_found(client_socket)
            else:
                get_user(client_socket,query)
        elif parmalink=='/user' and method=='OPTIONS':
            assert user_id is not None
            options_user(client_socket)
        elif parmalink=='/user' and method=='DELETE':
            assert user_id is not None
            delete_user(client_socket,user_id)
        elif parmalink=='/user' and method=='PUT':
            assert user_id is not None
            put_user(client_socket,msg_body_dict,user_id)
        

        # 클라이언트에게 응답
        # client_socket.sendall("welcome!".encode())

        # 클라이언트 소켓 종료  
        client_socket.close()  
