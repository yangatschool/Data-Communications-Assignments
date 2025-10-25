#!/usr/bin/env python3
#udp echo server

import socket
import sys

#server binding details
serverIP = "192.168.1.87"
serverPort = 4399
#max data size to receive
bufferSize = 2048

def main():
    #create UDP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #bind socket to IP and port
        serverSocket.bind((serverIP, serverPort))
    except OSError as errorMSG:
        #handle bind errors
        print(f"failed to bind {serverIP}:{serverPort} -> {errorMSG}")
        sys.exit(1)

    print(f"Server listening on {serverIP}:{serverPort} (UDP)")

    try:
        #main server loop
        while True:
            #receive data from client
            data, clientAddr = serverSocket.recvfrom(bufferSize)
            #skip empty data
            if not data:
                continue
            #print received message
            print(f"received from {clientAddr}: {data.decode()}")
            #send uppercase response back to client
            serverSocket.sendto(data.upper(), clientAddr)
    except KeyboardInterrupt:
        #handle user interrupt (Ctrl+C)
        print("\nserver shutting down")
    finally:
        #always close socket
        serverSocket.close()
        print("socket closed")

if __name__ == "__main__":
    main()