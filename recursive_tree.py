import turtle


__version__ = 0.9


class Turtle(turtle.Turtle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, visible=False)
        self.speed(30)
        self.pensize(5)
        self.pencolor("black")
        self.rt(-90)
        self.penup()
        self.sety(-310)
        self.pendown()

    def backward(self, distance: int):
        self.back(distance)

    def forward(self, distance: int):
        super().forward(distance)

    def rotate(self, angle: int):
        self.rt(angle)


class Tree:

    def __init__(self, t: Turtle, branches: list):
        self.turtle = t
        self.number = 0
        self.save = 0
        self.branches = branches
        self.length = self.update_length()
        self.data = []
        self.angle = 20

    def draw(self):
        self.branch()

    def branch(self):
        if self.number == len(self.branches):
            self.turtle.rotate(45)
            self.turtle.forward(10)
            self.turtle.backward(10)

            self.turtle.rotate(-90)
            self.turtle.forward(10)
            self.turtle.backward(10)
        else:
            self.update_length()
            self.turtle.forward(self.length)
            self.number += 1
            self.store()
            self.left()
            self.restore()
            self.right()

    def left(self):
        self.turtle.rotate(-self.angle)
        self.turtle.forward(self.length)
        self.branch()

    def right(self):
        self.turtle.rotate(self.angle)
        self.turtle.forward(self.length)
        self.branch()

    def update_length(self):
        self.length = self.branches[self.number] * 5 + 10
        return self.length

    def get(self):
        copy = self.data[-1]
        del self.data[-1]
        return copy

    def set(self, data):
        self.turtle.setx(data[0])
        self.turtle.sety(data[1])
        self.turtle.setheading(data[2])
        self.number = data[3]

    def restore(self):
        self.turtle.penup()
        self.set(self.get())
        self.turtle.pendown()

    def store(self):
        self.data.append((self.turtle.xcor(), self.turtle.ycor(), self.turtle.heading(), self.number))


class Screen:

    def __init__(self, size: (int, int), color: str = "white"):
        turtle.title("Recursive Tree")
        self.screen = turtle.Screen()
        self.screen.setup(*size)

        self.canvas = turtle.getscreen()
        self.canvas.screensize(size[0] - 10, size[1] - 10, bg=color)
        self.canvas.update()

    def loop(self):
        self.canvas.mainloop()

    def update(self):
        self.canvas.update()


my_turtle = Turtle()


def fact(n: int):
    while n > 0:
        yield n
        n -= 1


def main():
    branches = int(input("Number of branches: "))
    stack = list(fact(branches))
    tree = Tree(Turtle(), stack)
    screen = Screen((1080, 640), "white")
    print("Drawing...")
    screen.update()
    tree.draw()
    screen.loop()


if __name__ == '__main__':
    main()
