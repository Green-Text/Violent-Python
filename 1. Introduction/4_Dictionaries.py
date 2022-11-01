services = {"ftp":21, "ssh":22, "smtp":25, "http":80}

print(services.keys())
print(services.items())
print(services.__contains__("http"))
print(services["http"])

print("[+] Found vuln with FTP port {p}!".format(p=services["ftp"]))