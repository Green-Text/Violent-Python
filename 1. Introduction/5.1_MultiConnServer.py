import sys
import socket
import selectors
import types

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("Accepted connection from {a}".format(a=addr))
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn,events,data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection at {a}...".format(a=data.addr))
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("Echoing {d} to {a}...".format(d = str(data.outb), a = data.addr))            
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]



if "__main__" == __name__:
    selector = selectors.DefaultSelector()

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host,port))
    lsock.listen()
    print("Listenting on {o}".format(o=(host,port)))
    lsock.setblocking(False)
    selector.register(lsock, selectors.EVENT_READ, data = None)
    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Exiting!")    # Ctlr + c
    finally:
        selector.close()
    