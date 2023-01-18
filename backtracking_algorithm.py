import random
import pygame
from typing import List, Tuple, TypeVar


Coordinates = Tuple[int, int]


pygame.init()


class Stack:
    """
    LIFO: Last In First Out
    """

    _T = TypeVar("_T")

    def __init__(self):
        self.stack: 'List[Stack._T]' = []

    def get_data(self) -> 'Stack._T':
        return self.stack.pop(-1)

    def add(self, data: 'Stack._T'):
        self.stack.append(data)


class MainApp:

    SPEED = 60

    def __init__(self):
        self.screen_size = (1024, 640)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF)
        pygame.display.set_caption("Backtracking algorithm for mazes.")
        self.running = True
        self.maze = Maze(self)
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.maze.update()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(5 * self.SPEED)


class Maze:

    def __init__(self, app: MainApp):
        self.app = app
        self.tiles = {}
        for x in range(self.app.screen_size[0] // Tile.SIZE):
            for y in range(self.app.screen_size[1] // Tile.SIZE):
                self.tiles[x, y] = Tile((x, y))
        self.tracker = Tracker(self)

    def update(self):
        self.tracker.update()
        for tile in self.tiles.values():
            tile.display(self.app.screen)


class Tile:

    SIZE = 32

    def __init__(self, coordinates: 'Coordinates'):
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.rect = pygame.Rect(*[c * self.SIZE for c in coordinates], self.SIZE, self.SIZE)
        self.east = True
        self.south = True
        self.visited = False

    def display(self, screen: pygame.Surface):
        self.image.fill("white")
        x = self.SIZE // 8
        if self.east:
            self.image.fill("black", (self.SIZE - x, 0, x, self.SIZE))
        if self.south:
            self.image.fill("black", (0, self.SIZE - x, self.SIZE, x))
        screen.blit(self.image, self.rect)

    def visit(self):
        self.visited = True


class Tracker:

    @staticmethod
    def is_accessible(tile: 'Tile') -> bool:
        return tile is not None and not tile.visited

    def __init__(self, maze: 'Maze', position: 'Coordinates' = None):
        self.maze = maze
        if position is None:
            position = (0, 0)
        self.x, self.y = 0, 0
        self.history = Stack()
        self.goto(self.maze.tiles.get(position))

    def accessible_neighbor(self, tile: 'Tile') -> 'List[Tile]':
        accessible = []

        def get(x_, y_):
            return self.maze.tiles.get((x_, y_), None)

        def check(tile_: Tile):
            if self.is_accessible(tile_):
                accessible.append(tile_)

        if tile is not None:
            x = tile.rect.x // Tile.SIZE
            y = tile.rect.y // Tile.SIZE
            check(get(x, y-1))
            check(get(x+1, y))
            check(get(x, y+1))
            check(get(x-1, y))

        return accessible

    def find(self):
        while True:
            try:
                data = self.history.get_data()
                if self.accessible_neighbor(data):
                    self.goto(data)
                    self.update()
                    break
            except IndexError:
                break

    def goto(self, tile: 'Tile'):
        tile.visit()
        old = self.maze.tiles.get((self.x, self.y))
        self.history.add(tile)

        x = tile.rect.x // Tile.SIZE
        y = tile.rect.y // Tile.SIZE

        if x < self.x:
            tile.east = False
        elif x > self.x:
            old.east = False
        elif y < self.y:
            tile.south = False
        elif y > self.y:
            old.south = False

        self.x, self.y = tile.rect.x // Tile.SIZE, tile.rect.y // Tile.SIZE

    def update(self):
        accessible = self.accessible_neighbor(self.maze.tiles.get((self.x, self.y)))

        if accessible:
            self.goto(random.choice(accessible))
        else:
            self.find()


main_app = MainApp()

if __name__ == '__main__':
    main_app.run()

pygame.quit()
