import zipfile
from threading import Thread
import argparse
# Run 1
# This is the most basic version of the program.
# zFile will be assigned to EV.zip
# Since the password, i.e.: "secret", is already known, all files are extracted.
"""
zFile = zipfile.ZipFile("EV.zip")
zFile.extractall(pwd="secret")
"""

# Run 2
# But what if the given password was wrong? Then the zipfile wouldn't be opened!
# Hence, this version of the code utilizes try / chatch to illustrate if the program failed.
"""
zFile = zipfile.ZipFile("EV.zip")
try:
    zFile.extractall(pwd="secret")
except Exception, e:
    print e
"""

# Run 3
# This version enhances the try / catch mechanism of the previous iteration of the code by enabling it to read from a
# Dictionary file with the aid of passwordFile variable.With that bein said, all the lines are read of such a file with 
# the aid of a password variable. Furthermore, the program then tries to open the zip file with the aquired password. 
# If it fails, exeption occurs but the program continues; otherwise, the password is shown and the script terminates.
"""
zFile = zipfile.ZipFile("EV.zip")
passwordFile = open("Dictionary.txt")
for password in passwordFile.readlines():
    tmp = password.strip("\n")
    try:
        zFile.extractall(pwd=tmp)
        print("[+] Password = {r}".format(r = tmp))
        break
    except Exception, e:
        pass
"""

# Run 4
# This enhanced iteration of the already described program utilizes functions, as with: extractFile, wich has the two (2)
# parameters:
#   1. zFile: variable assigned to the zip file.
#   2. password: one of the passwords of the dictionary.
"""
def extractFile(zFile,password):
    try:
        zFile.extractall(pwd=password)
        return password
    except:
        return

def main():
    zFile = zipfile.ZipFile("EV.zip")
    passFile = open("Dictionary.txt")
    for line in passFile.readlines():
        password = line.strip("\n")
        guess = extractFile(zFile,password)
        if guess:
            print("[+] Password = {r}".format(r = guess))
            break
if __name__ == "__main__":
    main()
"""

# Run 5 (Multi Threading or Parallelism)
# This version of the program tackles the need for performance. It does this by using the threading function of Thread so as
# to enable the program to test all the passwords of the Dictionary file at once with extractAll function. 
"""
def extractFile(zFile, password):
    try:
        zFile.extractall(pwd= password)
        print("[+] Password = {r}".format(r = password))
    except:
        pass

def main():
    zFile = zipfile.ZipFile("EV.zip")
    passFile = open("Dictionary.txt")
    for p in passFile.readlines():
        password = p.strip("\n")
        t = Thread(target = extractFile, args =(zFile,password))
        t.start()
if __name__ == "__main__":
    main()
"""

# Run 6
# This is the last iteration of the program. It utilizes all that was learned before in conjunction with an additional 
# functionality, that of adding options to the python file when called in the terminal.
def extractFile(zFile,password):                                                                                    # Function to extract zipfile
    try:                                                                                                            # Try case to extact the contents of
        zFile.extractall(pwd=password)                                                                              # file with password parameter.
        print("[+] Password = {r}".format(r = str(password, "utf-8")))                                              # Output the password's plaintext.
    except:                                     
        pass                                                                                                        # If exception occurs, continue program.

def main():
    parser = argparse.ArgumentParser("usage%prog -f <name of zipfile> -d <name of dictionary>")                     # zipCracker.py -f <zipfile> -d <dictionary>
    parser.add_argument('-f', dest = 'zipName', type=str, help = 'specify zip file name with extension')             # Argument for zipfile name
    parser.add_argument('-d', dest = 'dictName', type=str, help = 'specify dictionary file name with extension')     # Argument for dictionary name
    args = parser.parse_args()   
    print(args)
    type(args)
    if (args.zipName == None) or (args.dictName == None):                                                            # If no arguments have been defined on terminal
        parser.print_help()                                                                                         # output the usage of the script.
        exit(0)                                                                                                     # Exit the program.
    else:
        zipName = args.zipName                                                                                      # Else create new variables and assign such arguments
        dictName = args.dictName                                                                                    # to themselves.
    zFile = zipfile.ZipFile(zipName)                                                                                # Open zipfile under the name assigned to zipFile variable.                         
    passFile = open(dictName)                                                                                       # Open the Dictionary file under dictName.
    for line in passFile.readlines():                                                                               # Read each of the lines of Dictionary File.
        password = bytes(line.strip("\n"), "utf-8")
        t = Thread(target=extractFile, args = (zFile, password))                                                    # Create a thread to try and open the zipFile with all 
        t.start()                                                                                                   # passwords at "once".
if __name__ == "__main__":
    main()