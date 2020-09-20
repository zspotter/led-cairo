import cairo
import time

from rgbmatrix import RGBMatrixOptions
from cairo_matrix import CairoMatrix
from math import sin, pi
from random import random
from colorsys import hsv_to_rgb, hls_to_rgb


def ease_io_quad(perc):
    if perc < 0.5:
        return 2 * perc * perc
    else:
        return (4 - 2 * perc) * perc - 1

def hex_to_rgb(h):
    return tuple(int(h.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))

candy = [hex_to_rgb(h) for h in ['#f72585', '#7209b7', '#3a0ca3', '#4361ee', '#4cc9f0']]
fire = [hex_to_rgb(h) for h in ['#220901','#621708','#941b0c','#bc3908','#f6aa1c']]

# Listed with `$ fc-list : family`
font_families = [
    'DejaVu Sans Mono',
    'DejaVu Sans',
    'DejaVu Serif',
    'Droid Sans Fallback',
    'FreeMono',
    'FreeSans',
    'FreeSerif',
    'Liberation Mono',
    'Liberation Sans',
    'Liberation Serif',
    'Noto Mono',
    'Piboto Condensed',
    'Piboto',
    'Piboto Light',
    'Piboto Thin',
    'PibotoLt',
    'Quicksand Light',
    'Quicksand Medium',
    'Quicksand',
]

class WavesMatrix(CairoMatrix):
    def draw(self, ctx):
        ctx.set_operator(cairo.Operator.ADD)
        ctx.set_source_rgb(*fire[1])
        self.draw_wave(ctx, 1)
        ctx.set_source_rgb(*fire[0])
        self.draw_wave(ctx, -1.4)
        ctx.set_operator(cairo.Operator.OVER)
        ctx.set_source_rgb(*fire[4])
        draw_time(ctx)

    def draw_wave(self, ctx, offset):
        segments = 64
        points = [None] * (segments * 2)
        for i in range(segments+1):
            x = i / segments
            perc_from_edge = min(x, abs(1 - x)) / 0.5
            y = sin(x * 10 + offset * self.tick / 700) / 4
            y = y * ease_io_quad(perc_from_edge) + 0.5
            width = 0.2 * perc_from_edge
            points[i] = (x, y - width)
            points[segments * 2 - i - 1] = (x, y + width)

        ctx.move_to(*points[0])
        for p in points:
            ctx.line_to(*p)
        ctx.fill()

    def draw_wave2(self, ctx, offset):
        segments = 64
        for i in range(segments + 1):
            x = i / segments
            y = sin((x * 10 + offset * self.tick / 500)) / 2 + 0.5
            perc_from_edge = min(x, abs(1 - x)) / 0.5
            y *= ease_io_quad(perc_from_edge)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
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
        ctx.set_line_width(0.15)
        ctx.set_source_rgb(*palette[2])
        segments = 64
        for i in range(segments):
            x = i / segments
            y =  0.5 + 0.2 * sin((x + rate * self.tick) * 10)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
        ctx.stroke()

class WindTrail(CairoMatrix):
    preserve = True
    darken = (2/255, 2/255, 2/255, 0.5)
    particles = [(random(), random()) for i in range(500)]

    def draw(self, ctx):
        if self.tick % 2 == 0:
            self.fade(ctx)

        ctx.set_operator(cairo.Operator.OVER)
        ctx.set_line_cap(cairo.LineCap.ROUND)
        ctx.set_line_width(0.01)
        ctx.set_source_rgb(*hsv_to_rgb(lfo(self.tick/100, 0.3, 0.6), 0.7, 0.6))
        for i, (x, y) in enumerate(self.particles):
            nx = lfo(self.tick/100, 0.5/1000, 1/1000) + x
            ny = lfo((self.tick + pi)/100, 0.5/1000, 1/1000) + y
            ctx.move_to(x, y)
            ctx.line_to(nx, ny)
            ctx.stroke()
            if nx >= 1:
                nx -= 1
            if ny >= 1:
                ny -= 1
            self.particles[i] = (nx, ny)

        ctx.set_source_rgb(0, 0, 0)
        draw_time(ctx)

    def fade(self, ctx):
        ctx.set_operator(cairo.Operator.DIFFERENCE)
        ctx.set_source_rgba(*self.darken)
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()


def lfo(t, low=0, high=1):
    return (high - low) * (0.5 + sin(t) / 2) + low

def draw_time(ctx, family='Piboto Condensed', size=0.6):
    font_opt = ctx.get_font_options()
    font_opt.set_antialias(cairo.Antialias.NONE)
    ctx.set_font_options(font_opt)
    ctx.select_font_face(family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    set_font_size_scaled(ctx, size)
    show_text_centered(ctx, time.strftime('%-I:%M'))

def set_font_teeny(ctx):
    font_opt = ctx.get_font_options()
    font_opt.set_antialias(cairo.Antialias.NONE)
    ctx.set_font_options(font_opt)
    ctx.select_font_face('Teeny Tiny Pixls', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    set_font_size_scaled(ctx, 0.15)

def show_text_centered(ctx, text):
    matrix = ctx.get_matrix()
    ext = ctx.text_extents(text)
    x = 0.5 - (ext.width/2 + ext.x_bearing)
    y = 0.5 - (ext.height/2 + ext.y_bearing)
    ctx.move_to(x, y)
    ctx.show_text(text)

def set_font_size_scaled(ctx, size):
    ctx.set_font_size(size)
    matrix = ctx.get_font_matrix()
    matrix.xx *= 0.5 # skew horizontal on 2:1 ratio
    ctx.set_font_matrix(matrix)


def main():
    options = RGBMatrixOptions()
    options.gpio_slowdown = 3
    options.brightness = 50
    options.rows = 32
    options.cols = 64

    # matrix = BandsMatrix(options=options)
    matrix = WindTrail(options=options)

    matrix.run()


if __name__ == '__main__':
    main()
