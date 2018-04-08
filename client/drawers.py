import sdl2

SCALE_DOWN = 100000
RECOMMENDED_WIDTH = 20

def pulse_render(screen, scrno, data, colours=[
        (000, 000, 000, 255),
        (255, 255, 255, 255)]):
    ratio = sum([sum(data[0]), sum(data[1])]) / len(data[0]) / SCALE_DOWN
    def segratio(i):
        return int(min((colours[1][i] - colours[0][i]) * ratio + colours[0][i]), 255)
    colour = (segratio(0), segratio(1), segratio(2), segratio(3))
    screen.setcolour(colour)
    sdl2.SDL_RenderClear(screen.sdlrenderer)

def updown_render(screen, scrno, data, colours=[
        (96, 210, 255, 255),
        (200, 200, 200, 255),
        (200, 000, 000, 255)]):
    width, height = screen.dimensions
    sect_width = width / len(data[0]) * scrno
    bars_each = int(len(data[0]) / scrno)
    screen.setcolour(colours[0])
    for i, channel in enumerate(data):
        for j, datum in enumerate(channel[screen.n * bars_each:(screen.n + 1) * bars_each]):
            screen.setcolour(colours[j % 2 if sect_width > RECOMMENDED_WIDTH else 0])
            bar = sdl2.SDL_Rect(
                    int(j * sect_width),
                    height // 2,
                    int(sect_width) + 1,
                    int((-1) ** i * datum * height // 2 // SCALE_DOWN))
            sdl2.SDL_RenderFillRect(screen.sdlrenderer, bar)
    screen.setcolour(colours[2])
    sdl2.SDL_RenderDrawLine(screen.sdlrenderer, 0, height // 2, width, height // 2)

def oscillo_render(screen, scrno, data, colours=[(255, 0, 0, 255), (0, 0, 255, 255)]):
    width, height = screen.dimensions
    sect_width = width / (len(data[0]) - 1)
    for i, channel in enumerate(data):
        screen.setcolour(colours[i])
        prev = None
        for j, datum in enumerate(channel):
            point = (int(sect_width * (j - 1)),
                    height // 2 + (-1) ** i * datum * height // 2 // SCALE_DOWN)
            if prev is not None:
                sdl2.SDL_RenderDrawLine(screen.sdlrenderer, prev[0], prev[1], point[0], point[1])
            prev = point
