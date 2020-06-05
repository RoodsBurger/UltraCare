from bluetooth import *
import json
import sys
import threading
import time

def recv(client_sock, exit_event):
    while exit_event.is_set():
        data = client_sock.recv(1024).decode()
        print("received: " + str(data))
    sys.exit()


def connection():

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    print("Waiting fior connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()

    print("Accepted connection from ", client_info)
    user_input = ""

    exit_event = threading.Event()
    exit_event.set()
    recv_thread = threading.Thread(target=recv, args=(client_sock,exit_event), daemon=True)
    recv_thread.start()

    while user_input != 'exit()':
        try:
            user_input = input("Message or exit():")
            client_sock.send(user_input)
            print("sending: " + str(user_input))

        except IOError:
            pass

    exit_event.clear()
    print("Disconnected from" + str(client_info))

    client_sock.close()
    server_sock.close()
    sys.exit()


while True:

    connection_thread = threading.Thread(target=connection, args=())
    connection_thread.start()
    connection_thread.join()
