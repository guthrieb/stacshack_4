#!/bin/env python3
import json
import sdl2
import struct
import socket
import random
import sdl2.ext
import sys

from drawers import *

class Events:
    def poll(self):
        self.events = []
        for event in sdl2.ext.get_events():
            self.events.append(event)

class Client:
    def __init__(self, ip, port, index):
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.sock.setblocking(True)
        self.remainder = ''

    def receive(self):
        text = self.remainder
        while True:
            mess = self.sock.recv(1024).decode()
            text += mess
            i = text.find('|')
            if not i == -1:
                split = text.split('|')
                self.remainder = split[-1]
                data = json.loads(split[-2])
                print(len(data))
                return data

class Screen:
    def __init__(self, n, dimensions):
        self.window = sdl2.ext.Window("visualiser", dimensions, flags = sdl2.SDL_WINDOW_RESIZABLE)
        self.renderer = sdl2.ext.Renderer(self.window)
        self.n = n

    @property
    def width(self):
        return self.window.size[0]

    @property
    def height(self):
        return self.window.size[1]

    @property
    def dimensions(self):
        return self.window.size

    @property
    def sdlrenderer(self):
        return self.renderer.sdlrenderer

    def setcolour(self, colour):
        self.renderer.color = sdl2.ext.Color(*colour)

    def show(self):
        self.window.show()

class Renderer:
    def __init__(self, n, dimensions):
        self.fg = (255, 255, 255, 255)
        self.bg = (000, 000, 000, 255)
        self.screens = []
        for i in range(0, n):
            screen = Screen(i, dimensions)
            self.screens.append(screen)
            screen.show()

    def draw(self, data):
        for screen in self.screens:
            screen.setcolour(self.bg)
            sdl2.SDL_RenderClear(screen.sdlrenderer)
            # pulse_render(screen, len(self.screens), data)
            updown_render(screen, len(self.screens), data)
            # oscillo_render(screen, len(self.screens), data)
            sdl2.SDL_RenderPresent(screen.renderer.sdlrenderer)

def loop(client, renderer, events):
    while True:
        events.poll()
        data = client.receive()
        renderer.draw(data)

def main(args):
    sdl2.ext.init()

    host_ip = args[1]
    port = int(args[2])
    index = args[3]
    style = args[4]

    client = Client(host_ip, port, index)
    renderer = Renderer(2, (800, 600))
    events = Events()
    loop(client, renderer, events)

    return 0

def hello(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("138.251.29.205", 5005))
    print("bound")
    while True:
        print(sock.recv(10240).decode())

def test(args):
    sdl2.ext.init()
    renderer = Renderer((800, 600))
    events = Events()
    while True:
        a = []
        b = []
        for i in range(1, 300):
            a.append(random.randint(0, 50000))
            b.append(random.randint(0, 50000))
        renderer.draw([a, b])
        events.poll()

if __name__ == '__main__':
    # sys.exit(test(sys.argv))
    # sys.exit(hello(sys.argv))
    sys.exit(main(sys.argv))
