import numpy
import math
import cairo

def shapes(ctx):
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.set_source(pat)
    ctx.fill()

    ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

    ctx.move_to(0, 0)
    # Arc(cx, cy, radius, start_angle, stop_angle)
    ctx.arc(0.2, 0.1, 0.1, -math.pi / 2, 0)
    ctx.line_to(0.5, 0.1)  # Line to (x,y)
    # Curve(x1, y1, x2, y2, x3, y3)
    ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
    ctx.close_path()

    ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
    ctx.set_line_width(0.02)
    ctx.stroke()

def x(ctx):
    ctx.translate(1, 1)
    ctx.move_to(0, 0)
    ctx.line_to(1, 1)
    ctx.move_to(0, 1)
    ctx.line_to(1, 0)

    ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
    ctx.set_line_width(0.02)
    ctx.stroke()

def spiral(ctx, width, height):
    wd = .02 * width
    hd = .02 * height

    width -= 2
    height -= 2

    ctx.move_to(width + 1, 1 - hd)
    for i in range(9):
        ctx.rel_line_to(0, height - hd * (2 * i - 1))
        ctx.rel_line_to(-(width - wd * (2 * i)), 0)
        ctx.rel_line_to(0, -(height - hd * (2 * i)))
        ctx.rel_line_to(width - wd * (2 * i + 1), 0)

    ctx.set_source_rgb(0, 0, 1)
    ctx.stroke()

def text_demo(cr, width, height):
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

    cr.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    cr.set_source(pat)
    cr.fill()


    cr.set_line_width(0.04)

    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(0.35)

    cr.move_to(0.04, 0.53)
    cr.show_text("Hello")

    cr.move_to(0.27, 0.65)
    cr.text_path("void")
    cr.set_source_rgb(0.5, 0.5, 1)
    cr.fill_preserve()
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(0.01)
    cr.stroke()

    # draw helping lines
    cr.set_source_rgba(1, 0.2, 0.2, 0.6)
    cr.arc(0.04, 0.53, 0.02, 0, 2 * math.pi)
    cr.arc(0.27, 0.65, 0.02, 0, 2 * math.pi)
    cr.fill()


def get_buf(width, height):
    surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.scale(width, height)  # Normalizing the canvas

    text_demo(ctx, width, height)
    # surface.write_to_png("example.png")  # Output to PNG

    surface.flush()
    buf = surface.get_data()
    # data = numpy.ndarray(shape=(WIDTH, HEIGHT),
    #                      dtype=numpy.uint32,
    #                      buffer=buf)
    return buf.tolist()
