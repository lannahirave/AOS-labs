#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import logging


class Server:

    def __init__(self):
        try:
            HOST = '127.0.0.1'
          
            PORT = 1025+9
            utf = 'utf-8'
            self.utf = utf
            logging.getLogger("Server")
            logging.basicConfig(filename="myServer.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info("Server started")

            server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            count, operations = 0, []
            try:
                server.bind((HOST, PORT))
            except OSError:
                print("Host is used.")
                logging.warning('HOST IS USED. ')
                exit()
            server.listen(1)
            conn, addr = server.accept()
            print('Connected:', addr)
            logging.info("Connected to a client.")
            conn.send(self.welcome_message().encode(utf))
            logging.info("Sent the welcome message.")
            print('Listening...')
            logging.info('Listening to a client.')
            try:
                while True:
                    data = conn.recv(256).decode(utf)
                    logging.info(f'Received message: {data}')
                    if not data:
                        break
                    answer, count, operations = self.process(
                        data[1:], count, operations)
                    print(f"Send answer:\n{answer}")
                    if answer is None:
                        logging.info("Process function broke at some moment.")
                        raise IOError
                    if "<STOP>" in answer:
                        conn.send(answer.encode(utf))
                        logging.info(
                            f'Send answer:\n{answer}\n In which found stop command.')
                        logging.info("Connection closed.")
                        break
                    conn.send(answer.encode(utf))
                    logging.info(f'Sent answer:\n{answer}')
            except:
                print("ERROR.")
                logging.info("Caught en error. Closing connection.")
                conn.send("<STOP>".encode(utf))
        finally:
            try:
                conn.close()
            except Exception as e:
                print(f' !Exception {e}')
                logging.warning(f'{e}')
            print("Connection closed.")
            logging.info("Server stopped!\n" + "#" * 10 + "\n")

    def process(self, data: str, count: int, operations: list):
        try:
            results = ''
            flag = True
            counter = count
            oper = operations
            if data == '' or data.replace(' ', '') == '':
                return "=Wrong input", counter, oper

            elif ';' in data:
                arr = data.split(';')
                for i in arr:
                    if i.replace(' ', '') == '':
                        results += "Wrong input;"

                    elif ['who'] == arr[arr.index(i)].split():
                        results += self.whoami()
                    elif ['stop'] == arr[arr.index(i)].split():
                        results += '<STOP>;'
                        return self.print_message(results, oper, counter), counter, oper
                    else:
                        for letter in i:
                            if not (letter.isdigit() or letter in '+-*/= '):
                                results += "Wrong input;"
                                flag = False
                                break
                        if not flag:
                            flag = True
                            continue
                        else:
                            try:
                                result = str(eval(i))
                                oper.append(int(result))
                                results += result + ';'
                                counter += 1
                            except ZeroDivisionError:
                                results += "ZeroDivisonError;"
                            except:
                                results += "Wrong input;"
            else:
                arr = ''
                if data.replace(' ', '') == '':
                    results += 'Wrong input;'
                elif ['who'] == data.split():
                    results += self.whoami()
                elif ['stop'] == data.split():
                    results += '<STOP>;'
                    return self.print_message(results, oper, counter), counter, oper
                else:
                    for i in data:
                        if not (i.isdigit() or i in '+-*/= '):
                            results += "Wrong input;"
                            flag = False
                            break
                    if not flag:
                        flag = True
                        return '=' + results, counter, oper
                    try:
                        result = str(eval(data))
                        oper.append(int(result))
                        results += result + ';'
                        counter += 1
                    except ZeroDivisionError:
                        results += "ZeroDivisonError;"
                    except:
                        results += "Wrong input;"
            return '=' + results, counter, oper
        except Exception as e:
            return f"={e}"

    def print_message(self, results: str, array: list, count: int):
        if len(array) > 0:
            avg = sum(array)/len(array)
            text = '=' + f'min: {min(array)}, max: {max(array)}, avg: {avg} \
count: {count}\n'
        else:
            text = f'count: {count}\n'
        return text + results

    def welcome_message(self):
        welcome = '''Send any basic math sequence and get a result back.\n Example: "2+2; 4/4;" and so on.\n'''
        return welcome

    def whoami(self):
        who = 'Student of K-24 Nikitin Ruslan Valerii №9 Calculator;'
        return who


def main():
    root = Server()


if __name__ == "__main__":
    main()
