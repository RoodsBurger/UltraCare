#!/usr/bin/env python3

from bluetooth import *
import json
import sys
import threading
import time
import os

#def recv(client_sock, exit_event):
#    try:
#        while not exit_event.is_set():
#            data = client_sock.recv(2048).decode("iso-8859-2")
#            print(str(data))
#            if(data == "exit()"):
#                exit_event.set()

#    except IOError:
#        pass

#    sys.exit()


def connection():

    os.system('sudo hciconfig hci0 piscan')

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    print("Waiting fior connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()

    print("Accepted connection from ", client_info)
    #user_input = ""

    #exit_event = threading.Event()
    #recv_thread = threading.Thread(target=recv, args=(client_sock,exit_event), daemon=True)
    #recv_thread.start()

    #exit_event.clear()

    #while user_input != 'exit()' and not exit_event.is_set():
    #    try:
    #        user_input = input("Message or exit():")
    #        client_sock.send(user_input)
    #        print("sending: " + str(user_input))

    #    except IOError:
    #        pass

    data = ""
    json_string = ""
    data_size = "0"
    try:
        while True:
            #if json_string == "": data_size = client_sock.recv(5).decode("utf-8","ignore")
            data = client_sock.recv(1024).decode("utf-8","ignore")#"iso-8859-2")
            #os.system('sudo hciconfig hci0 noscan')
            #print(str(data.decode("utf-8","ignore")))
            #print("\n\n\n" + data_size + "\n\n\n")
            #print("\n\n\n" + str(len(json_string)) + "\n\n\n")
            json_string = json_string + data
            if data[-6:]=="mqtt()":#len(json_string) >= int(data_size):
                os.system('mount -o remount,rw /dev/mmcblk0p2/')
                json_string = json_string[:len(json_string)-6]
                #print(json_string)
                with open("/home/smdin/mqtt_setup.json", 'w') as f:
                    f.write(json_string)
                json_string = ""
                os.system('mount -o remount,ro /dev/mmcblk0p2/')
            elif data[-6:]=="setp()":
                os.system('mount -o remount,rw /dev/mmcblk0p2/')
                json_string = json_string[:len(json_string)-6]
                #print(json_string)
                with open("/home/smdin/device_setup.json", 'w') as f:
                    f.write(json_string)
                json_string = ""
                os.system('mount -o remount,ro /dev/mmcblk0p2/')
            elif data[-6:]=="remq()":
                try:
                    with open("/home/smdin/mqtt_setup.json", "r") as json_file:
                        json_string = json.dumps(json.load(json_file))
                    try:
                        client_sock.send((json_string+"exit()").encode("utf-8","ignore"))
                    except IOError:
                        pass
                except IOError:
                    try:
                        client_sock.send("exit()".encode("utf-8","ignore"))
                    except IOError:
                        pass
                json_string = ""
            elif data[-6:]=="reio()":
                try:
                    with open("/home/smdin/device_setup.json", "r") as json_file:
                        json_string = json.dumps(json.load(json_file))
                    try:
                        client_sock.send((json_string+"exit()").encode("utf-8","ignore"))
                    except IOError:
                        pass
                except IOError:
                    try:
                        client_sock.send("exit()".encode("utf-8","ignore"))
                    except IOError:
                        pass
                json_string = ""
            elif data[-6:]=="rebt()":
                os.system('reboot')


    except IOError:
        pass

    print("Disconnected from" + str(client_info))

    client_sock.close()
    server_sock.close()
    sys.exit()


while True:
    try:
        connection_thread = threading.Thread(target=connection, args=())
        connection_thread.start()
        connection_thread.join()
    except IOError:
        pass
