import socket

# create a socket object
s = socket.socket()

# get the IP address of the receiver
receiver_ip = '127.0.0.1'
receiver_port = 12345

# bind the socket to the receiver IP address and port number
s.bind((receiver_ip, receiver_port))

# listen for incoming connections
s.listen()

# accept a connection from a sender
connection, address = s.accept()

# receive the message from the sender
message = connection.recv(1024).decode()
print('Received message: ' + message)

# close the connection and the socket
connection.close()
s.close()