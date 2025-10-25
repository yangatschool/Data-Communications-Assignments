#!/usr/bin/env python3
#tcp echo server

import socket
import sys

#server binding details
serverIP = "192.168.1.87"
serverPort = 4399
#max data size to receive
bufferSize = 2048
#max pending connections in queue
backlog = 5 

def handle_client(connection, clientAddr):
    try:
        print(f"connection from {clientAddr}")
        #client handling loop
        while True:
            #receive data from client
            data = connection.recv(bufferSize)
            #client disconnected if no data
            if not data:
                print(f"{clientAddr} disconnected")
                break
            #print received message
            print(f"received from {clientAddr}: {data.decode()}")
            #send uppercase response back to client
            connection.sendall(data.upper())
    except ConnectionResetError:
        #handle client disconnection
        print(f"connection reset by {clientAddr}")
    finally:
        #close client connection
        connection.close()

def main():
    #create TCP socket
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #allow socket reuse
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        #bind socket to IP and port
        listenSocket.bind((serverIP, serverPort))
    except OSError as errorMSG:
        #handle bind errors
        print(f"failed to bind {serverIP}:{serverPort} -> {errorMSG}")
        sys.exit(1)

    #start listening for connections
    listenSocket.listen(backlog)
    print(f"tcp server listening on {serverIP}:{serverPort}")

    try:
        #main server loop
        while True:
            #accept new client connection
            connection, clientAddr = listenSocket.accept()
            #handle client in function
            handle_client(connection, clientAddr)
    except KeyboardInterrupt:
        #handle user interrupt (Ctrl+C)
        print("\nserver shutting down")
    finally:
        #close listening socket
        listenSocket.close()
        print("listening socket closed")

if __name__ == "__main__":
    main()