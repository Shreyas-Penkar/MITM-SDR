import socket

UDP_IP = "127.0.0.1"
UDP_PORT_SINK =6666
UDP_PORT_SOURCE =7777
UDP_PORT_REV_SHELL=8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT_SINK))
sock.settimeout(0.5)

print("Starting UDP Sink: ")
while True:
    try:
        data, addr = sock.recvfrom(1472) 
        print(data
        if (data.decode())[0:3] == '%@#':
            sock.sendto(data, (UDP_IP,UDP_PORT_REV_SHELL))        
        else:
            sock.sendto(data, (UDP_IP,UDP_PORT_SOURCE))
    except socket.timeout:
        pass