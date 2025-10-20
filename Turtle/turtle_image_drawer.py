import turtle as t
from typing import Tuple
from pathlib import Path
import sys


def draw_1(bitmap):
    homex, homey = t.pos()
    for row in bitmap:
        t.penup()
        t.setpos((homex, homey))
        for i, pixel in enumerate(row, start=0):
            if pixel == 1:
                pass
            else:
                t.setpos(homex + i, homey)
                t.pendown()
                t.forward(1)
                t.penup()
        homey -= 1


def draw_2(bitmap):
    homex, homey = t.pos()
    for row in bitmap:
        t.penup()
        t.setpos((homex, homey))
        pd = False
        for i, pixel in enumerate(row):
            if pixel == 1:
                if pd:
                    t.penup()
                    pd = False
            else:
                t.setpos(homex + i, homey)
                if not pd:
                    t.pendown()
                    pd = True
                t.forward(1)
        if pd:
            t.penup()
        homey -= 1


def draw_3(bitmap):
    only_flips = []
    for row in bitmap:
        flip_row = []
        cur_pix = 1
        for i, pixel in enumerate(row):
            if pixel != cur_pix:
                cur_pix = pixel
                flip_row.append(i)
        only_flips.append(flip_row)

    homex, homey = t.pos()
    for row in only_flips:
        t.penup()
        t.setpos((homex, homey))
        for i, flip in enumerate(row):
            if i % 2 == 1:
                continue
            else:
                t.setpos(homex + row[i], homey)
                t.pendown()
                if len(row) > i + 1:
                    t.forward(row[i + 1] - row[i])
                else:
                    t.forward(len(bitmap[0]) - row[i])
                t.penup()
        homey -= 1


import numpy as np
from PIL import Image


def convert_to_mono(path: str, size: Tuple[int, int]):
    img = Image.open(path).convert("L")
    img = img.resize(size)
    arr = np.array(img)
    threshold = 128
    monochrome_table = (arr < threshold).astype(int)
    return monochrome_table


if __name__ == "__main__":
    t.speed("fastest")
    t.penup()
    t.setpos(-400, 400)
    script_dir = Path(__file__).resolve().parent
    img_path = script_dir / "happy.jpeg"
    if not img_path.exists():
        print(f"Image not found: {img_path}")
        sys.exit(1)

    try:
        table = convert_to_mono(str(img_path), (26, 26))
    except Exception as e:
        print(f"Failed to open or convert image: {e}")
        sys.exit(1)

    function_to_use = 1
    functions = {0: draw_1, 1: draw_2, 2: draw_3}
    functions[function_to_use](table)
    t.done()
