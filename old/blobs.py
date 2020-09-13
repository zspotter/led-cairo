import argparse
import time
import sys
import os
import math
import noise

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from fonts import Font
import pycairo


def square(matrix):
    def rotate(x, y, angle):
        return (
            x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle)
        )

    def scale_col(val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    cent_x = matrix.width / 2
    cent_y = matrix.height / 2

    rotate_square = min(matrix.width, matrix.height) * 1.41

    display_square = min(matrix.width, matrix.height) * 0.7
    min_display = cent_x - display_square / 2
    max_display = cent_x + display_square / 2

    deg_to_rad = 2 * 3.14159265 / 360
    rotation = 0

    def get_pixel(matrix, x, y, rotation):
        (rot_x, rot_y) = rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
        if x >= min_display and x < max_display and y >= min_display and y < max_display:
            return (scale_col(x, min_display, max_display), 255 - scale_col(y, min_display, max_display), scale_col(y, min_display, max_display))
        else:
            return (0, 0, 0)

    return get_pixel


COLOR = (209, 97, 60)
BLACK = (0, 0, 0)

# Size of features
SX = 20
SY = 20
# Delta position per frame
DX = 0.05
DY = 0.1
DZ = 0.005
def simp(matrix, x, y, t):
    n = (1 + noise.snoise3((t * DX + x) / SX, (t * DY + y) / SY, t * DZ)) / 2
    n = (int(n * 100) % 100) / 100
    # if int(n * 100) % 100 >= (math.sin(t/30) / 2.0 + 1) * 25 + 40:
    return scale(COLOR, n)
    # return BLACK


def make_text(matrix, text):
    height = matrix.height
    width = matrix.width
    font = Font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', height//2)
    text_bitmap = font.render_text(text)
    x_off = (width - text_bitmap.width) // 2
    y_off = (height - text_bitmap.height) // 2
    def pixel(matrix, x, y, t):
        text_x = x - x_off
        text_y = y - y_off
        text_p = None
        if text_y < 0 or text_x < 0 or text_y >= text_bitmap.height or text_x >= text_bitmap.width:
           text_p = False
        else:
            text_p = text_bitmap.get(text_x, text_y)
        if text_p != (simp(matrix, y, x, t/2.0) == BLACK):
            return COLOR
        return BLACK

    return pixel


############

def scale(color, perc):
    return (int(color[0]*perc), int(color[1]*perc), int(color[2]*perc))

############

def make_matrix(width, height, brightness):
    options = RGBMatrixOptions()
    options.gpio_slowdown = 2
    options.disable_hardware_pulsing = True
    options.brightness = brightness
    options.rows = height
    options.cols = width
    return RGBMatrix(options = options)


def run(matrix, get_pixel):
    tick = 0
    offset_canvas = matrix.CreateFrameCanvas()
    while True:
        for x in range(0, matrix.width):
            for y in range(0, matrix.height):
                (r, g, b) = get_pixel(matrix, x, y, tick)
                offset_canvas.SetPixel(x, y, r, g, b)

        offset_canvas = matrix.SwapOnVSync(offset_canvas)
        tick += 1


def run_cairo(matrix):
    buf = pycairo.get_buf(matrix.width, matrix.height)
    offset_canvas = matrix.CreateFrameCanvas()
    while True:
        for i in range(0, len(buf), 4):
            b, g, r, a = buf[i], buf[i+1], buf[i+2], buf[i+3]
            y = int(i / 4 / matrix.width)
            x = int((i / 4) % matrix.width)
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)


def main():
    w, h = 64, 32
    matrix = make_matrix(w, h, 50)
    # run(matrix, simp)
    run_cairo(matrix)

if __name__ == "__main__":
    main()
