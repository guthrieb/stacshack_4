import sdl2
import struct
import socket
import random
import sdl2.ext
import sys

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
        self.sock.setblocking(False)

    def receive(self):
        try:
            data, addr = self.recvfrom(1024)
            return json.loads(data)
        except json.decoder.JSONDecodeError as e:
            print(message)
            sys.exit(1)

class Screen:
    def __init__(self, dimensions):
        self.window = sdl2.ext.Window("visualiser", dimensions, flags = sdl2.SDL_WINDOW_RESIZABLE)
        self.renderer = sdl2.ext.Renderer(self.window)

    @property
    def width(self):
        return self.window.size[0]

    @property
    def height(self):
        return self.window.size[1]

    def setcolour(self, colour):
        self.renderer.color = sdl2.ext.Color(*colour)

class Renderer:
    def __init__(self, dimensions):
        self.fg = (255, 255, 255, 255)
        self.bg = (000, 000, 000, 255)
        self.screen = Screen(dimensions)
        self.screen.window.show()

    def draw(self, data):
        self.screen.setcolour(self.bg)
        sdl2.SDL_RenderClear(self.screen.renderer.sdlrenderer)
        width = self.screen.width
        height = self.screen.height
        sect_width = width / len(data)
        self.screen.setcolour(self.fg)
        for i, datum in enumerate(data):
            bar = sdl2.SDL_Rect(
                    int(i * sect_width),
                    height // 2,
                    int(sect_width) + 1,
                    -datum * height // 200)
            sdl2.SDL_RenderFillRect(self.screen.renderer.sdlrenderer, bar)
        sdl2.SDL_RenderPresent(self.screen.renderer.sdlrenderer)

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
    renderer = Renderer((800, 600))
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
        data = []
        for _ in range(1, 300):
            data.append(random.randint(-100, 100))
        renderer.draw(data)
        events.poll()

if __name__ == '__main__':
    sys.exit(test(sys.argv))
