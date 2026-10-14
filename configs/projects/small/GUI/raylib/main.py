import logging

from pyray import *

logging.basicConfig(level=logging.ERROR)

set_trace_log_level(LOG_ERROR)

GAP = 1
set_config_flags(FLAG_WINDOW_UNDECORATED | FLAG_WINDOW_RESIZABLE)

init_window(500, 400, "UwU")
set_target_fps(60)
set_window_state(FLAG_WINDOW_UNDECORATED)
set_window_state(FLAG_WINDOW_TRANSPARENT)
set_window_state(FLAG_WINDOW_RESIZABLE)


def middle_point(coords: tuple) -> tuple:
    a, b = coords
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def next_triangle(coords: tuple, color=RED) -> tuple:
    a, b, c = coords
    d = middle_point((a, c))
    e = middle_point((b, c))
    f = middle_point((a, b))
    draw_triangle_lines(d, e, f, color)
    return (d, e, f)


def next_set(first: tuple, second: tuple):
    a, b, c = first
    d, e, f = second
    return (a, f, d), (f, b, e), (d, e, c)


def count_coeff(depth: int) -> float:
    depth -= 1
    ans = 0
    for i in range(depth):
        ans += 3 ** (i + 1)
    return 255 / ans


counter = 1


def loop(triangle: tuple, depth: int, coeff=1):
    global counter
    if depth == 0:
        return
    counter += 1
    # coeff = count_coeff(depth)
    second_triangle = next_triangle(
        triangle
        # triangle, (round(coeff * counter), round(coeff * counter), round(coeff * counter))
    )

    for setted_triangle in next_set(triangle, second_triangle):
        loop(setted_triangle, depth - 1)


def start_triangle() -> tuple:
    width, height = get_render_width(), get_render_height()
    first = (GAP, height - GAP)
    second = (width - GAP, height - GAP)
    coords = (first, second, (middle_point((first, second))[0], GAP))
    draw_triangle_lines(coords[0], coords[1], coords[2], RED)
    return coords


while not window_should_close():
    set_window_state(FLAG_WINDOW_UNFOCUSED)
    begin_drawing()
    clear_background(BLANK)
    loop(start_triangle(), 6)
    end_drawing()
close_window()
