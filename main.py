import cairo
import math
import time

from rgbmatrix import RGBMatrixOptions
from cairo_matrix import CairoMatrix


def ease_io_quad(perc):
    if perc < 0.5:
        return 2 * perc * perc
    else:
        return (4 - 2 * perc) * perc - 1

def hex_to_rgb(h):
    return tuple(int(h.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))

candy = list(map(hex_to_rgb, ['#f72585', '#7209b7', '#3a0ca3', '#4361ee', '#4cc9f0']))
fire = list(map(hex_to_rgb, ["#220901","#621708","#941b0c","#bc3908","#f6aa1c"]))

class WavesMatrix(CairoMatrix):
    def draw(self, ctx):
        ctx.set_operator(cairo.Operator.ADD)
        ctx.set_source_rgb(1, 0, 0)
        self.draw_wave(ctx, 1)
        ctx.set_source_rgb(0, 1, 0)
        self.draw_wave(ctx, -1.4)
        ctx.set_source_rgb(0, 0, 1)
        self.draw_wave(ctx, 2)

        ctx.set_operator(cairo.Operator.XOR)
        ctx.set_source_rgb(1, 1, 1)
        draw_time(ctx)


    def draw_wave(self, ctx, offset):
        segments = 64
        for i in range(segments):
            x = i / segments
            y = math.sin((x + offset * self.tick / 300) * 10) / 2 + 0.5
            perc_from_edge = min(x, abs(1 - x)) / 0.5
            y *= ease_io_quad(perc_from_edge)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
        ctx.line_to(1, 0)
        ctx.close_path()
        ctx.fill()


class BandsMatrix(CairoMatrix):
    def draw(self, ctx, palette=fire[::-1]):
        ctx.set_operator(cairo.Operator.ADD)
        ctx.set_source_rgb(*palette[2])
        self.draw_band(ctx, 1/550)
        ctx.set_source_rgb(*palette[3])
        self.draw_band(ctx, 1/500)

        ctx.set_operator(cairo.Operator.XOR)
        ctx.set_source_rgb(*palette[0])
        draw_time(ctx)


    def draw_band(self, ctx, rate):
        ctx.set_line_width(0.1)
        segments = 64
        for i in range(segments):
            x = i / segments
            y =  0.5 + 0.2 * math.sin((x + rate * self.tick) * 10)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
        ctx.stroke()



def draw_time(ctx):
    font_opt = ctx.get_font_options()
    font_opt.set_antialias(cairo.Antialias.NONE)
    ctx.set_font_options(font_opt)
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(0.35)
    show_text_centered(ctx, time.strftime('%-I:%M'))


def show_text_centered(ctx, text):
    ext = ctx.text_extents(text)
    x = 0.5 - (ext.width/2 + ext.x_bearing)
    y = 0.5 - (ext.height/2 + ext.y_bearing)
    ctx.move_to(x, y)
    ctx.show_text(text)


def main():
    options = RGBMatrixOptions()
    options.gpio_slowdown = 2
    options.disable_hardware_pulsing = True
    options.brightness = 50
    options.rows = 32
    options.cols = 64

    matrix = BandsMatrix(options=options)
    # matrix = WavesMatrix(options=options)

    matrix.run()


if __name__ == "__main__":
    main()
