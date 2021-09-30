#!/usr/bin/python3
import socket


class Client:

    def __init__(self,):
        HOST = '127.0.0.1'
        PORT = 1025+9

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        sock.connect((HOST, PORT))
        data = sock.recv(256).decode('utf-8')
        print(data)

        while True:
            sock.send(('=' + input('Send request:\n=')).encode('utf-8'))
            data = sock.recv(256).decode('utf-8')
            print('Answer:\n', data)
            if "<STOP>" in data:
                sock.close()
                break
        print("Connection closed.")

    @staticmethod
    def reconnect():
        while True:
            answer = input("Do you want to try to reconnect? Y/n: ")
            if answer.lower() in 'yn':
                break
        if answer.lower() == 'y':
            return True
        else:
            return False


def main():
    client = Client()


if __name__ == "__main__":
    main()
