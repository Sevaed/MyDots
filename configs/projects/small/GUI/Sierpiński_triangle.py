from tkinter import *

WIDTH = 500
HEIGHT = 400
GAP = 4

LINE_WIDTH = 2

root = Tk()
root.resizable(False, False)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.attributes(alpha=0.5)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root, background="grey")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))


# def rgb_to_hex(r,g,b):
#     return f"{r:04x}"
def create_triangle(coords: tuple, color="black"):
    a, b, c = coords
    canvas.create_line(a[0], a[1], b[0], b[1], width=LINE_WIDTH)
    canvas.create_line(b[0], b[1], c[0], c[1], width=LINE_WIDTH)
    canvas.create_line(a[0], a[1], c[0], c[1], width=LINE_WIDTH)


def middle_point(coords: tuple) -> tuple:
    a, b = coords
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def next_triangle(coords: tuple, color="black"):
    a, b, c = coords
    d = middle_point((a, c))
    e = middle_point((b, c))
    f = middle_point((a, b))
    create_triangle((d, e, f), color)
    return (d, e, f)


def next_set(first: tuple, second: tuple):
    a, b, c = first
    d, e, f = second
    return (a, f, d), (f, b, e), (d, e, c)


left_x = GAP
right_x = WIDTH - GAP
top_x = (left_x + right_x) / 2

start_triangle = (
    (left_x, HEIGHT - GAP),
    (right_x, HEIGHT - GAP),
    (top_x, GAP),
)

counter = 1

create_triangle(start_triangle)


def loop(triangle, depth):
    global counter
    if depth == 0:
        return
    coeff = 65535 / depth
    counter += 1
    # second_triangle = next_triangle(triangle, round(counter * coeff))
    second_triangle = next_triangle(triangle)

    for setted_triangle in next_set(triangle, second_triangle):
        loop(setted_triangle, depth - 1)


loop(start_triangle, 4)

print(counter)
root.mainloop()
