import turtle
from typing import Tuple
from pathlib import Path
import sys
import numpy as np
from PIL import Image

t = turtle.Turtle()
t.speed("fastest")


class FractalTurtle:
    def __init__(self, t_obj=None):
        self.t = t_obj or turtle.Turtle()
        try:
            self.t.speed("fastest")
        except Exception:
            pass

    def moj(self, x):
        if x < 2:
            return
        self.moj(x / 1.1)
        for i in range(6):
            self.t.forward(x)
            self.t.left(60)
        for i in range(6):
            self.t.forward(x)
            self.t.right(60)
        self.t.forward(x)
        self.t.left(20)

    def Kwadrat(self, x):
        for i in range(4):
            self.t.forward(x)
            self.t.left(90)

    def KwadratFraktal(self, x):
        z = 1
        for y in range(x):
            for i in range(4):
                self.t.forward(z)
                self.t.left(90)
            z = z * 1.1

    def Sierpisnki(self, x):
        if x < 5:
            return
        for i in range(3):
            self.Sierpisnki(x / 2)
            self.t.forward(x)
            self.t.left(120)

    def test(self, x):
        if x < 10:
            return
        for i in range(3):
            self.test(x / 2)

            self.t.left(60)
            self.t.forward(x / 3)
            self.t.right(60)
            self.t.forward(x / 3)
            self.t.left(60)
            self.t.forward(x / 3)


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


def convert_to_mono(path: str, size: Tuple[int, int]):
    img = Image.open(path).convert("L")
    img = img.resize(size)
    arr = np.array(img)
    threshold = 128
    monochrome_table = (arr < threshold).astype(int)
    return monochrome_table


fr = FractalTurtle(t)
# # ZADANIE 1
# x = 60
# fr.Kwadrat(x)

# # ZADANIE 2
# x = 60
# fr.KwadratFraktal(x)

# # ZADANIE 3
# x = 250
# fr.Sierpisnki(x)

# # ZADANIE 4a
# x = 400
# fr.moj(x)

# # ZADANIE 4b
# x = 400
# fr.test(x)

# # ZADANIE 5
# t.penup()
# script_dir = Path(__file__).resolve().parent
# img_path = script_dir / "happy.jpeg"
# if not img_path.exists():
#     print(f"Image not found: {img_path}")
#     sys.exit(1)
# try:
#     table = convert_to_mono(str(img_path), (26, 26))
# except Exception as e:
#     print(f"Failed to open or convert image: {e}")
#     sys.exit(1)
# draw_3(table)
# turtle.done()
