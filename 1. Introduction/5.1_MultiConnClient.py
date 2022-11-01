import re
import sys
import socket
import selectors
import types

selector = selectors.DefaultSelector()
messages = [b"Hello there!\n\t\t-Obi One Kenobi",
b"Have you heard the story of Darth Plagueis the Wise?\n\t\t-Darth Sidious"]

def start_Connections(host, port, num_Connections):
    server_addr = (host, port)
    for i in range(0, num_Connections):
        conId = i + 1
        print("Starting connection {id} to {server_addr}".format(id = conId, server_addr=server_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)                # To eliminate blocking exception
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connId = conId, msg_Total = sum(len(m) for m in messages), recv_Total = 0, messages = messages.copy(), outb = b"")
        selector.register(sock, events, data = data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print("Received {d} from {id}".format(d = recv_data, id=data.connId))
            data.recv_Total += len(recv_data)
        if not recv_data or data.recv_Total == data.msg_Total:
            print("Closing cinnection {id}".format(id = data.connId))
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("Sending {do} to connection {id}".format(do=str(data.outb), id=data.connId))
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <host> <port> <number of connections>")
        sys.exit(1)
    host, port, nConn = sys.argv[1:4]
    start_Connections(host, int(port), int(nConn))
    try:
        while True:
            events = selector.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)
            if not selector.get_map():          # Check if socket is already being monitored
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Exiting!")    # Ctrl + c
    finally:
        selector.close()