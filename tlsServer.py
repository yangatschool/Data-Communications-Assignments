#!/usr/bin/env python3
#tls echo server

import socket
import ssl
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
            if not data:
                print(f"{clientAddr} disconnected")
                break

            #print received message
            print(f"received from {clientAddr}: {data.decode()}")
            #send uppercase response back to client
            connection.sendall(data.upper())

    except ConnectionResetError:
        print(f"connection reset by {clientAddr}")

    finally:
        #close client connection
        try:
            connection.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        connection.close()

def main():
    #create tcp socket
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #allow socket reuse
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        #bind socket to ip and port
        listenSocket.bind((serverIP, serverPort))
    except OSError as errorMSG:
        print(f"failed to bind {serverIP}:{serverPort} -> {errorMSG}")
        sys.exit(1)

    #start listening for connections
    listenSocket.listen(backlog)
    print(f"tls server listening on {serverIP}:{serverPort}")

    #create tls server context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #load certificate and private key
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    try:
        #main server loop
        while True:
            #accept new client connection
            clientSocket, clientAddr = listenSocket.accept()

            try:
                #wrap accepted socket with tls
                tlsSocket = context.wrap_socket(clientSocket, server_side=True)
            except ssl.SSLError as e:
                print(f"tls handshake failed from {clientAddr}: {e}")
                clientSocket.close()
                continue

            #handle client
            handle_client(tlsSocket, clientAddr)

    except KeyboardInterrupt:
        print("\nserver shutting down")

    finally:
        #close listening socket
        listenSocket.close()
        print("listening socket closed")

if __name__ == "__main__":
    main()
