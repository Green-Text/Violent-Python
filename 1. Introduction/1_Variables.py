banner = "FreeFloat FTP Server"
portList = [21, 22, 80, 110]
portOpen = True

print("Validating the variables data types, i.e:\n"+
"1. Banner {b} => {bT}\n".format(b = banner, bT = type(banner))+
"2. Port List {pL} => {pLT}\n".format(pL = portList, pLT = type(portList))+
"3. Port {p} => {pT}\n".format(p = portList[0], pT=type(portList[0]))+
"4. Is Port Open? :/ {oP} => {oPT}".format(oP = portOpen, oPT = type(portOpen)))
