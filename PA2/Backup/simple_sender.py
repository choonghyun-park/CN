import socket

# create a socket object
s = socket.socket()

# get the IP address of the receiver
receiver_ip = '127.0.0.1'
receiver_port = 12345

# connect to the receiver
s.connect((receiver_ip, receiver_port))

# send a message to the receiver
message = 'Hello, receiver!'
s.send(message.encode())

# close the socket
s.close()