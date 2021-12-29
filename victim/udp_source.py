import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 7777

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

while(1):
    message=input("Enter Message: ")
    for i in range(20):    
        try:
	        sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
        
        
        except socket.timeout:
            pass



