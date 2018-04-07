#!/usr/bin/env python
import socket
import _thread as th

TCP_IP = '138.251.29.205'
TCP_PORT = 1234
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

def thread_handler(conn, addr):
    message = "Hello, World!"
    conn.send(message.encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while True:
        print("Waiting for connection")
        conn, addr = s.accept()
        th.start_new_thread(thread_handler, conn, addr)
        print("Connection Accepted")
    conn.close()

if __name__ == "__main__":
    main()
