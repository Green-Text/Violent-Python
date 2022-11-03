import socket

headerSize = 10

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect_ex(("127.0.0.1", 65432))

message = ""
is_New = True
try:
    while True:
        buffer = soc.recv(16)
        if buffer:
            if is_New:
                print("New message length: {l}".format(l = buffer[:headerSize]))
                messageLength = int(buffer[:headerSize])
                is_New = False

            message += buffer.decode("UTF-8")

            if len(message) - headerSize == messageLength:
                print("Recieved message from server: {m}".format(m = message[headerSize:]))
                is_New = True
                message= ""
        else:
            soc.close()
            break
except KeyboardInterrupt:
    print("Key accepted! Disconnecting from server!")
    soc.close()