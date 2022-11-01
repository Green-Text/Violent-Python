portList = []

portList.append(21)
portList.append(80)
portList.append(443)
portList.append(25)
print(portList)

portList.sort()
print(portList)

print("[+] There are {n} ports to scan before 80.".format(n=portList.index(80)))

portList.remove(443)
print(portList)

print("[+] Scanning {n} total ports.".format(n=len(portList)))