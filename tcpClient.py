#!/usr/bin/env python3
#tcp echo client

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
    #create TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #set socket timeout
    clientSocket.settimeout(timed)
    try:
        #try to connect to server
        try:
            clientSocket.connect((serverIP, serverPort))
        except (ConnectionRefusedError, OSError) as e:
            #handle connection errors
            print(f"unable to connect to {serverIP}:{serverPort} -> {e}")
            return

        #get message from command line or user input
        message = None
        if len(sys.argv) >= 2:
            #use command line arguments as message
            message = " ".join(sys.argv[1:])
        else:
            #get message from user input
            message = input("enter message to send to server: ")

        #check if message is empty
        if not message:
            print("no message entered")
            print("closing")
            return

        #send message to server
        clientSocket.sendall(message.encode())
        try:
            #wait for server response
            data = clientSocket.recv(bufferSize)
            if not data:
                #server closed connection
                print("server closed connection without replying")
            else:
                #print received data
                print(f"received from server: {data.decode()}")
        except socket.timeout:
            #handle timeout case
            print(f"no response within {timed} seconds (timeout)")
    except KeyboardInterrupt:
        #handle user interrupt (Ctrl+C)
        print("\nclient aborted by user")
    finally:
        #always close socket
        clientSocket.close()
        print("socket closed")

if __name__ == "__main__":
    main()