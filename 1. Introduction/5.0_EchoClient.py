import socket

host = "127.0.0.1"                  # IP used by server
port = 65432                        # Port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.connect((host,port))
    soc.sendall(b"Hello World!")    # Data buffer
    data = soc.recv(1024)
print("Received! ==> {d}".format(d=data))