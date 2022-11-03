import socket
import time
import selectors
import sys
import types

class EchoSever:
    def __init__(self, host, port, headerSize=10):
        self.host = host
        self.port = port
        self.headerSize = headerSize
        self.selector = selectors.DefaultSelector()
    
    def startServer(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen()
        print("Server listening on {o}.".format(o = (self.host, self.port)))
        self.serverSocket.setblocking(False)
        self.selector.register(self.serverSocket,selectors.EVENT_READ, data = None)
    
    def connectClient(self, externalSocket):
        clientSocket, addr = externalSocket.accept()
        print("Accepted connection from {a}".format(a = addr))
        clientSocket.setblocking(False)
        data = types.SimpleNamespace(addr = addr)
        events = selectors.EVENT_WRITE
        self.selector.register(clientSocket,events, data = data)
    
    def processClient(self, key, mask):
        clientSocket = key.fileobj
        try:
            if mask & selectors.EVENT_WRITE:
                message = "Welcome to the server!"
                message = f"{len(message):<{self.headerSize}}" + message
                clientSocket.send(bytes(message, "UTF-8"))
                try:
                    while True:                 # The While will halt the server per user. Need to find python synch info.
                        time.sleep(3)
                        message = "The time is {t}.".format(t = time.time())
                        message = f"{len(message):<{self.headerSize}}" + message
                        clientSocket.send(bytes(message, "UTF-8"))
                except KeyboardInterrupt:
                    print("Keyboard input accepted! Closing connection!")
        except Exception as e:
            print("Seems something happened with the connection {addr}".format(addr = key.data))
        self.selector.unregister(clientSocket)
        clientSocket.close()
if __name__ == "__main__":
    server = EchoSever("127.0.0.1", 65432)
    server.startServer()

    try:
        while True:
            events = server.selector.select(timeout=0)
            for key, mask in events:
                if key.data is None:
                    server.connectClient(key.fileobj)
                else:
                    server.processClient(key, mask)
    except KeyboardInterrupt:
        print("Key accepted! Halting server!")
    finally:
        server.selector.close()


