import turtle

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

# ZADANIE 5


turtle.done()
