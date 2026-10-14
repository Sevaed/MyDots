import logging
from math import sqrt

from pyray import *

logging.basicConfig(level=logging.ERROR)

set_trace_log_level(LOG_ERROR)

set_config_flags(
    FLAG_WINDOW_TRANSPARENT
    | FLAG_WINDOW_UNDECORATED
    | FLAG_WINDOW_TOPMOST
    | FLAG_WINDOW_UNFOCUSED
    | FLAG_WINDOW_MOUSE_PASSTHROUGH
)

GAP = 25

init_window(1920, 1080, "David")


def find_middle_point(a: tuple, b: tuple):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


class Line:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def middle_point(self):
        find_middle_point((self.a, self.b), (self.c, self.d))

    def angle_coeff(self):
        return (self.b - self.d) / (self.a - self.c)

    def y_intercept(self):
        return self.b - self.angle_coeff() * self.a


def find_triangle_middle_point(a: tuple, b: tuple, c: tuple):
    sas = find_middle_point(a, c)
    sys = find_middle_point(b, c)
    sas = Line(sas[0], sas[1], b[0], b[1])
    sys = Line(sys[0], sys[1], a[0], a[1])
    m1 = sas.angle_coeff()
    m2 = sys.angle_coeff()
    b1 = sas.y_intercept()
    b2 = sys.y_intercept()
    x = (b2 - b1) / (m1 - m2)
    return (x, m1 * x + b1)


def smart_shit(middle_point):
    sas = TRIANGLE_HEIGHT / 3 * 2
    y = middle_point[1] - sas
    return y


old = {"height": None, "middle_point": None, "triangle_height": None,"monitor":None}
while not window_should_close():
    begin_drawing()
    clear_background(BLANK)
    width, height = get_render_width(), get_render_height()
    middle_point = (width / 2, height / 2)
    TRIANGLE_HEIGHT = height - GAP * 2 - (height - GAP * 2) / 4
    TRIANGLE_WIDTH = round(TRIANGLE_HEIGHT * 2 / sqrt(3))
    new = {
        "height": height,
        "middle_point": middle_point,
        "triangle_height": TRIANGLE_HEIGHT,
        "monitor":get_current_monitor()
    }
    flag = False
    for k, v in old.items():
        if v != new[k]:
            old[k] = new[k]
            print(f"{k}:  {v} => {new[k]}")
            flag = True
    if flag:
        print("\n")
    y3 = smart_shit(middle_point)
    sas = TRIANGLE_HEIGHT / 3
    first = (
        (round(middle_point[0] - TRIANGLE_WIDTH / 2), round(y3 + TRIANGLE_HEIGHT)),
        (round(middle_point[0] + TRIANGLE_WIDTH / 2), round(y3 + TRIANGLE_HEIGHT)),
        (round(middle_point[0]), round(y3)),
    )
    middle_point = find_triangle_middle_point(
        first[0],
        first[1],
        first[2],
    )
    second = (
        (middle_point[0] - TRIANGLE_WIDTH / 2, first[2][1] + sas),
        (middle_point[0] + TRIANGLE_WIDTH / 2, first[2][1] + sas),
        (middle_point[0], first[1][1] + sas),
    )
    draw_triangle_lines(
        first[0],
        first[1],
        first[2],
        BLUE,
    )
    draw_triangle_lines(
        second[0],
        second[1],
        second[2],
        BLUE,
    )
    end_drawing()
