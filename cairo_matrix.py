import cairo
from rgbmatrix import RGBMatrix


class CairoMatrix(RGBMatrix):
    def run(self):
        self.tick = 0
        offset_canvas = self.CreateFrameCanvas()
        while True:
            surface = cairo.ImageSurface(cairo.Format.ARGB32, self.width, self.height)
            ctx = cairo.Context(surface)
            ctx.scale(self.width, self.height)

            self.draw(ctx)

            surface.flush()
            buf = surface.get_data().tolist()

            for i in range(0, len(buf), 4):
                b, g, r, a = buf[i], buf[i+1], buf[i+2], buf[i+3]
                y = int(i / 4 / self.width)
                x = int((i / 4) % self.width)
                offset_canvas.SetPixel(x, y, r, g, b)
            offset_canvas = self.SwapOnVSync(offset_canvas)
            self.tick += 1

    def draw(ctx):
        # Implement me!
        pass

