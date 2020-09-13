import cairo
import math


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


def main():
    width, height = 64, 32
    surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.scale(width, height)

    text_demo(ctx, width, height)

    surface.write_to_png("surface.png")


if __name__ == "__main__":
    main()
