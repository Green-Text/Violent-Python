import argparse
import socket
from threading import Thread
from threading import Semaphore

def connScan(targetHost,targetPort):
    screenLock = Semaphore()
    try:
        connectedSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectedSocket.create_connection((targetHost,targetPort))
        connectedSocket.send(b'ViolentPython\n')
        results = connectedSocket.recv(100).decode('utf-8')
        screenLock.acquire()
        print("[+] TCP open {r}".format(r = targetPort))
        print("[+] {r}".format(r = results))
        connectedSocket.close()
    except:
        screenLock.acquire()
        print("[-] TCP closed {r} port.".format(r = targetPort))
    finally:
        screenLock.release()
def portScan(targetHost, targetPorts):
    try:
        targetIP = socket.gethostbyname(targetHost)
    except:
        print("[-] Cannot resolve {r}. Unknown host.".format(r = targetHost))
        return
    try:
        targetName = socket.gethostbyaddr(targetIP)
        print("Scan results for {a}.".format(a = targetName[0]))
    except:
        print("Scan results for {a}.".format(a = targetIP))
    socket.setdefaulttimeout(1)
    for port in targetPorts:
        print("Scanning port {r}.".format(r = port))
        # connScan(tgtHost, int(tgtPort))
        t = Thread(target = connScan, args=(targetHost, int(port)))
        t.start()
def main():
    parser = argparse.ArgumentParser("usage %prog -H <target host> -p <target port>")
    parser.add_argument("-H", dest = "targetHost", type = str, help = "Specify target host")
    parser.add_argument("-p", dest = "targetPorts", type = str, help = "Specify target port(s) separated by commas")
    args = parser.parse_args()
    targetHost = args.targetHost
    targetPorts = str(args.targetPorts).split(",")
    if (targetHost == None) | (targetPorts[0] == None):
        print(parser.print_help())
        exit(0)
    portScan(targetHost,targetPorts)
if __name__ == "__main__":
    main()