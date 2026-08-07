import os
import curses
import re

MOUSES_LUA = os.path.expanduser("~/.config/hypr/config_files/mouses.lua")
FILE_CONTENT = re.compile(r"local mouses = \{.+\}", flags=re.DOTALL)

UP = [curses.KEY_UP, ord("k")]
DOWN = [curses.KEY_DOWN, ord("j")]
EXIT = [ord("q"), 27]
ENTER = [curses.KEY_ENTER, 10, 13, ord(" ")]

CHECKBOX_ENABLED = "[*] "
CHECKBOX_DISABLED = "[ ] "

if not os.path.exists(MOUSES_LUA):
    exit(f"Error: file {MOUSES_LUA} was not found")


def update_lua_config(mouses: dict):
    first = re.sub(r"[\{\}\' ']", "", str(mouses))
    second = (
        re.sub(r":", "=", first).replace("True", "true").replace("False", "false") + ","
    )
    content = f"""
    local mouses = {{{second}}}
    return mouses
    """
    with open(MOUSES_LUA, "w") as file:
        file.write(content)


def lua_table_parser(table: str) -> dict:
    mouses = {}
    first_pattern = re.compile(r"[\{ \n]")
    first = re.sub(first_pattern, "", table)
    second_pattern = re.compile(r"([^,}]+=[^,}]+)", flags=re.DOTALL)
    second = second_pattern.findall(first)
    for i in second:
        sas = i.split("=")
        if sas[1] == "false":
            sas[1] = ""
        mouses[sas[0]] = bool(sas[1])
    return mouses


def main(stdscr):
    curses.curs_set(0)
    active_selection = 0
    while True:
        stdscr.clear()
        with open(MOUSES_LUA, "r") as file:
            data = re.search(FILE_CONTENT, file.read()).group()
            if not data:
                exit("Wrong MOUSES_LUA")
        mouses = lua_table_parser(re.search(r"\{.+\}", data, flags=re.DOTALL).group())
        text = {}
        biggest = 1
        for mouse in mouses:
            if len(mouse) > biggest:
                biggest = len(mouse)
        for mouse in mouses:
            if mouses[mouse]:
                text[mouse] = CHECKBOX_ENABLED + mouse.center(biggest)
            else:
                text[mouse] = CHECKBOX_DISABLED + mouse.center(biggest)
        _, max_x = stdscr.getmaxyx()
        y = 0
        x = round(max_x / 2) - round((4 + biggest) / 2)
        mouses_list = {}
        for i, mouse in enumerate(text):
            to_print = text[mouse]
            mouses_list[i] = mouse
            if i == active_selection:
                stdscr.addstr(y, x, to_print, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, to_print)
            y += 1
        stdscr.refresh
        key = stdscr.getch()
        if key in DOWN:
            if active_selection < len(mouses) - 1:
                active_selection += 1
            else:
                active_selection = 0
        if key in UP:
            if active_selection > 0:
                active_selection -= 1
            else:
                active_selection = len(mouses) - 1
        if key in EXIT:
            exit(0)
        if key in ENTER:
            mouses[mouses_list[active_selection]] = not mouses[
                mouses_list[active_selection]
            ]
            update_lua_config(mouses)


curses.wrapper(main)
