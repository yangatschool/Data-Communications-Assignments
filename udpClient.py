#!/usr/bin/env python3
#udp echo client

import socket
import sys

#server connection details
serverIP = "192.168.1.87"
serverPort = 4399
#max data size to receive
bufferSize = 2048
#socket timeout in seconds
timed = 5

def main():
    #create UDP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #set socket timeout
    clientSocket.settimeout(timed)

    try:
        #get user input
        message = input("Enter message to send to server: ")
        #check if message is empty
        if not message:
            print("no message entered; exiting")
            return

        #send message to server
        clientSocket.sendto(message.encode(), (serverIP, serverPort))
        try:
            #wait for server response
            data, serverAddr = clientSocket.recvfrom(bufferSize)
            #print received data
            print(f"received from {serverAddr}: {data.decode()}")
        except socket.timeout:
            #handle timeout case
            print(f"no response from server after {timed}s.")
    except KeyboardInterrupt:
        #handle user interrupt (Ctrl+C)
        print("\nclient aborted by user")
    finally:
        #always close socket
        clientSocket.close()
        print("socket closed")

if __name__ == "__main__":
    main()