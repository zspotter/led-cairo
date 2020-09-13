import cairo
import math
import time

from rgbmatrix import RGBMatrixOptions
from cairo_matrix import CairoMatrix


class WavesMatrix(CairoMatrix):
    def draw(self, ctx):
        ctx.set_operator(cairo.Operator.ADD)
        ctx.set_source_rgb(1, 0, 0)
        self.draw_wave(ctx, 0)
        ctx.set_source_rgb(0, 1, 0)
        self.draw_wave(ctx, 40)
        ctx.set_source_rgb(0, 0, 1)
        self.draw_wave(ctx, 70)

        ctx.set_operator(cairo.Operator.XOR)
        ctx.set_source_rgb(1, 1, 1)
        self.draw_time(ctx)


    def draw_wave(self, ctx, offset):
        segments = 64
        for i in range(segments):
            x = i / segments
            y = math.sin((x + offset + self.tick / 300) * 10) / 2 + 0.5
            perc_from_edge = min(x, abs(1 - x)) / 0.5
            y *= ease_io_quad(perc_from_edge)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
        ctx.line_to(1, 0)
        ctx.close_path()
        ctx.fill()


    def draw_time(self, ctx):
        font_opt = ctx.get_font_options()
        font_opt.set_antialias(cairo.Antialias.NONE)
        ctx.set_font_options(font_opt)
        ctx.select_font_face('monospace', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.35)
        show_text_centered(ctx, time.strftime('%-I:%M'))


def show_text_centered(ctx, text):
    ext = ctx.text_extents(text)
    x = 0.5 - (ext.width/2 + ext.x_bearing)
    y = 0.5 - (ext.height/2 + ext.y_bearing)
    ctx.move_to(x, y)
    ctx.show_text(text)


def ease_io_quad(perc):
    if perc < 0.5:
        return 2 * perc * perc
    else:
        return (4 - 2 * perc) * perc - 1


def main():
    options = RGBMatrixOptions()
    options.gpio_slowdown = 2
    options.disable_hardware_pulsing = True
    options.brightness = 50
    options.rows = 32
    options.cols = 64

    matrix = WavesMatrix(options=options)
    matrix.run()


if __name__ == "__main__":
    main()
