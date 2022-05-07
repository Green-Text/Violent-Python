
import crypt

def testPass(cryptoPasswd):
    salt = cryptoPasswd[0:2]                                        # salt variable for hash password generation.
    dictionary = open("dictionary.txt", "r")                        # dictionary variable to read assigned dictionary.txt file.
    for word in dictionary.readlines():                             
        word =  word.strip("\n")                                    # If passwords contain "\n", extract them without such escape construct.
        cryptword = crypt.crypt(word,salt)                          # Create a new hashed password with each of the password in dictionary.txt file and the salt variable.
        if(cryptword == cryptoPasswd):                              # Check if the hash of the previously created hashed password and cryptoPasswd is the same. 
            print("[+] Found the password {r}".format(r = word))    # If same, then print the plaintext version of password.
            return
    print("[x] Password was not found!")                            # If all fails, output that plaintext password was not found.
    return

def main():
    # 1. passFile variable is set to read the assigned text file.
    # 2. Each of the lines of such file are read and passed down to line variable.
    # 3. If there is a ":" inside one of the lines then:
    # 3.1 The string of line is split into two from the location of ":".
    # 3.2 user variable is assigned the first half portion of string content.
    # 3.3 cryptoPasswd (Encrypted Password) variable is assigned the last half of the contents inside line variable.
    # 4. The name of the user is outputed to the screen.
    # 5. testPass is called asking for encrypted password parameter. 
    passFile = open("password.txt", "r")
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptoPasswd = line.split(":")[1].strip(" ")
            print("[*] Checking password for user {r}:".format(r = user))
            testPass(cryptoPasswd)

if __name__ == "__main__":
    main()
