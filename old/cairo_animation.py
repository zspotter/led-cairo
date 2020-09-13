import math

import threading
import time

import cairo


class Animator(Gtk.DrawingArea):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.connect("draw", self.do_drawing)
        self.tick = 0
        self.stopping = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def stop(self):
        self.stopping = True
        self.thread.join()

    def run(self):
        while not self.stopping:
            self.queue_draw()
            self.tick += 1
            time.sleep(60/1000)

    def do_drawing(self, widget, ctx):
        self.draw(ctx, self.get_allocated_width(), self.get_allocated_height())

    def draw(self, ctx, width, height):
        pass

class Waves(Animator):
    def draw(self, ctx, width, height):
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        ctx.set_operator(cairo.Operator.ADD)

        ctx.set_source_rgb(1, 0, 0)
        self.draw_wave(ctx, width, height, 0)
        ctx.set_source_rgb(0, 1, 0)
        self.draw_wave(ctx, width, height, 40)
        ctx.set_source_rgb(0, 0, 1)
        self.draw_wave(ctx, width, height, 70)

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_operator(cairo.Operator.OVER)
        self.draw_time(ctx, width, height)


    def draw_wave(self, ctx, width, height, offset):
        segments = 100
        for i in range(segments):
            x = i * width / segments 
            y = height * (math.sin((x + offset + self.tick) / 30) + 1) / 2
            perc_from_edge = min(x, abs(width - x)) / (width / 2)
            y *= ease_in_out_quad(perc_from_edge)
            if i == 0:
                ctx.move_to(x, y)
            ctx.line_to(x, y)
        ctx.close_path()
        ctx.fill()


    def draw_time(self, ctx, width, height):
        ctx.select_font_face('Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(height/2)
        ctx.move_to(width/5, height - height/4)
        ctx.show_text(time.strftime('%I:%M'))

def ease_in_out_quad(perc):
    return 2*perc*perc if perc<.5 else -1+(4-2*perc)*perc


def main():
    drawingarea = Waves()

    scale = 10
    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_default_size(scale * 64, scale * 32)
    win.add(drawingarea)

    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
