import cairo
import time
from PIL import Image
from rgbmatrix import RGBMatrix


class CairoMatrix(RGBMatrix):
    def run(self):
        self.tick = 0
        offset_canvas = self.CreateFrameCanvas()
        while True:
            # start = time.time()
            # TODO: add the option to use the same surface each frame, so that the draw function
            # can work ontop of the last frame
            surface = cairo.ImageSurface(cairo.Format.ARGB32, self.width, self.height)
            ctx = cairo.Context(surface)
            ctx.scale(self.width, self.height)

            self.draw(ctx)
            surface.flush()

            img = Image.frombuffer("RGBA", (surface.get_width(), surface.get_height()), surface.get_data().tobytes(), "raw", "BGRA", 0, 1).convert('RGB')
            offset_canvas.SetImage(img)

            # buf = surface.get_data().tolist()
            # for i in range(0, len(buf), 4):
            #     b, g, r = buf[i], buf[i+1], buf[i+2] # alpha = buf[i+3]
            #     y = int(i / 4 / self.width)
            #     x = (i / 4) % self.width
            #     offset_canvas.SetPixel(x, y, r, g, b)

            offset_canvas = self.SwapOnVSync(offset_canvas)
            self.tick += 1
            # print('Elapsed: ', (time.time() - start)*1000)

    def draw(ctx):
        # Implement me!
        pass

