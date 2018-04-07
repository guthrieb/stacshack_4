#!/usr/bin/env python
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("138.251.29.205", 1234))
    print("bound")
    while True:
        print("Receiving")
        print(sock.recv(1240).decode())

if __name__ == "__main__":
    main()
