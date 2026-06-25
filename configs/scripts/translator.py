#!/bin/python
import sys

keyboard_mapping = {
    "`": "ё",
    "~": "Ё",
    "1": "1",
    "!": "!",
    "2": "2",
    "@": '"',
    "3": "3",
    "#": "№",
    "4": "4",
    "$": ";",
    "5": "5",
    "%": "%",
    "6": "6",
    "^": ":",
    "7": "7",
    "&": "?",
    "8": "8",
    "*": "*",
    "9": "9",
    "(": "(",
    "0": "0",
    ")": ")",
    "-": "-",
    "_": "_",
    "=": "=",
    "+": "+",
    "q": "й",
    "Q": "Й",
    "w": "ц",
    "W": "Ц",
    "e": "у",
    "E": "У",
    "r": "к",
    "R": "К",
    "t": "е",
    "T": "Е",
    "y": "н",
    "Y": "Н",
    "u": "г",
    "U": "Г",
    "i": "ш",
    "I": "Ш",
    "o": "щ",
    "O": "Щ",
    "p": "з",
    "P": "З",
    "[": "х",
    "{": "Х",
    "]": "ъ",
    "}": "Ъ",
    "\\": "\\",
    "|": "/",
    "a": "ф",
    "A": "Ф",
    "s": "ы",
    "S": "Ы",
    "d": "в",
    "D": "В",
    "f": "а",
    "F": "А",
    "g": "п",
    "G": "П",
    "h": "р",
    "H": "Р",
    "j": "о",
    "J": "О",
    "k": "л",
    "K": "Л",
    "l": "д",
    "L": "Д",
    ";": "ж",
    ":": "Ж",
    "'": "э",
    '"': "Э",
    "z": "я",
    "Z": "Я",
    "x": "ч",
    "X": "Ч",
    "c": "с",
    "C": "С",
    "v": "м",
    "V": "М",
    "b": "и",
    "B": "И",
    "n": "т",
    "N": "Т",
    "m": "ь",
    "M": "Ь",
    ",": "б",
    "<": "Б",
    ".": "ю",
    ">": "Ю",
    "/": ".",
    "?": ",",
}

english_letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

lett = english_letters
my_dict = keyboard_mapping
revers = {}
layout = None


def check_layout(arg):
    global lett, layout
    for i in arg:
        if i in lett:
            layout = "EN"
            return layout
    layout = "RU"
    return layout


def main():
    global my_dict, layout
    lc_dict = {"c": "курва"}
    while True:
        inp = str(
            input("Введите текст с неправильной раскладкой или quit для выхода: \n")
        )
        if inp == "quit":
            break
        if check_layout(inp) == "EN":
            lc_dict = my_dict
        elif check_layout(inp) == "RU":
            lc_dict = reverse(my_dict)
        if bool(layout):
            answer = [lc_dict.get(i, i) for i in inp]
            print("".join(answer))


def reverse(par={}):
    dict_keys = list(par.keys())
    for i in dict_keys:
        key = my_dict.get(i)
        revers.update({key: i})
    return revers


def work(arg):
    wrk = ""
    for i in arg:
        wrk += f"{i} "
    arg = wrk
    global my_dict, layout
    lc_dict = {"c": "курва"}
    if check_layout(arg) == "EN":
        lc_dict = my_dict
    elif check_layout(arg) == "RU":
        lc_dict = reverse(my_dict)
    if bool(layout):
        answer = [lc_dict.get(i, i) for i in arg]
        print("".join(answer))


def check(arg):
    ans = ""
    for i in arg:
        print(i)
        ans += f"{i} "
    print(ans)


if __name__ == "__main__":
    work(sys.argv[1:])
    # check(sys.argv[1:])
    # main()
