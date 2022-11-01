import socket

host = "127.0.0.1"
port = 65432                        # Non priviliged ports are port > 1023

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((host, port))          # Associate socket with host and port number
    soc.listen()                    # Make server to listen for connections
    conn, addr = soc.accept()       # Make server accept connection requests.
                                    # It will return a socket (conn) that is what
                                    # will be used by the server to do operations.
    with conn:
        print("Connect by {a}...".format(a = addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    # Wait is used to kill process if no bytes are sent from the client.