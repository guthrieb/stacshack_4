#!/usr/bin/env python
import socket
import _thread as th
from AudioTransformer import handle_file
import json
import Config
import time
from file_player import Player

TCP_IP = '138.251.29.205'
TCP_PORT = Config.PORT
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
FILENAME = "test_files/test_muzzy.wav"

def thread_handler(conn, addr):
    results = handle_file(FILENAME)

    pl = Player()

    th.start_new_thread(pl.play_music, (FILENAME,))

    old_i = 0
    curFreq = 0
    for ent in results:
        data = ent
        while Player.i <= old_i:
            print("\n\n\n")
            print(Player.i)
            print(old_i)

        time.sleep(1 / 65)
        json_data = json.dumps([data]) + "|"
        old_i += 1
        print(json_data)
        conn.send(json_data.encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while True:
        print("Waiting for connection")
        conn, addr = s.accept()
        th.start_new_thread(thread_handler, (conn, addr))
        print("Connection Accepted")
    conn.close()

if __name__ == "__main__":
    main()
