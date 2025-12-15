#!/usr/bin/env python3
#tls echo client

import socket
import ssl
import sys

#server connection details
serverIP = "192.168.1.87"
serverPort = 4399

#max data size to receive
bufferSize = 2048

#socket timeout in seconds
timed = 5

def main():
    #create tcp socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #set socket timeout
    clientSocket.settimeout(timed)

    try:
        #try to connect to server
        try:
            clientSocket.connect((serverIP, serverPort))
        except (ConnectionRefusedError, OSError) as e:
            print(f"unable to connect to {serverIP}:{serverPort} -> {e}")
            return

        #create tls context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        #load server certificate
        context.load_verify_locations("server.crt")
        #wrap tcp socket with tls
        tlsSocket = context.wrap_socket(clientSocket, server_hostname=serverIP)

        #get message from command line or user input
        if len(sys.argv) >= 2:
            message = " ".join(sys.argv[1:])
        else:
            message = input("enter message to send to server: ")

        #check if message is empty
        if not message:
            print("no message entered")
            return

        #send message to server
        tlsSocket.sendall(message.encode())

        try:
            #wait for server response
            data = tlsSocket.recv(bufferSize)
            if not data:
                print("server closed connection without replying")
            else:
                print(f"received from server: {data.decode()}")
        except socket.timeout:
            print(f"no response within {timed} seconds (timeout)")

    except ssl.SSLError as e:
        print(f"tls error: {e}")

    except KeyboardInterrupt:
        print("\nclient aborted by user")

    finally:
        #close tls socket
        try:
            tlsSocket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        tlsSocket.close()
        print("socket closed")

if __name__ == "__main__":
    main()
