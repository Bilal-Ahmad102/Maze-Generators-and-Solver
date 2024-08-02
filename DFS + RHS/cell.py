import pyglet as pg
from pyglet.gl import *
import random
from pyglet.graphics import OrderedGroup

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cols = None
        self.rows = None
        self.lines = None
        self.fill = None
        self.flags = [True, True, True, True]  # [left, top, right, bottom]
        self.fill_color = None  # Start with no fill
        self.visited = False
    
    def index(self, i, j):
        if i < 0 or j < 0 or i > self.cols - 1 or j > self.rows - 1:
            return None
        return i + j * self.cols
    
    def checkNeighbours(self, grid):
        neighbours = []

        top    = grid[self.index(self.x, self.y - 1)] if self.index(self.x, self.y - 1) is not None else None
        right  = grid[self.index(self.x + 1, self.y)] if self.index(self.x + 1, self.y) is not None else None
        bottom = grid[self.index(self.x, self.y + 1)] if self.index(self.x, self.y + 1) is not None else None
        left   = grid[self.index(self.x - 1, self.y)] if self.index(self.x - 1, self.y) is not None else None

        if top and not top.visited:
            neighbours.append(top)
        if right and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.visited:
            neighbours.append(left)

        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None

    def show(self, w, cell_batch, lines_batch,wall_color):
        if self.lines is not None:
            self.lines.delete()
            self.lines = None
        if self.fill is not None:
            self.fill.delete()
            self.fill = None

        x1, y1 = self.x * w, self.y * w                 # bottom left corner
        x2, y2 = (self.x + 1) * w, (self.y + 1) * w     # top   right corner

        # Adjust the lines if this is the first row or first column
        x1 = x1 + 0.01 if self.x == 0 else x1       # First column, most left line
        y1 = y1 + 1 if self.y == 0 else y1          # First rows, most bottom line
        y2 = y2 - 5 if self.y == self.cols-0.1 else y2     # Last row, most top line

        # Draw filled rectangle if fill color is set
        if self.fill_color is not None:
            self.fill = cell_batch.add(4, GL_QUADS, OrderedGroup(0),
                ('v2f', (x1, y1, x2, y1, x2, y2, x1, y2)),
                ('c3B', self.fill_color * 4))

        vertices = []
        colors = []

        if self.flags[3]:  # Bottom
            vertices.extend([x1, y1, x2, y1])
            colors.extend(wall_color)
        if self.flags[2]:  # Right
            vertices.extend([x2, y1, x2, y2])
            colors.extend(wall_color)
        if self.flags[1]:  # Top
            vertices.extend([x2, y2, x1, y2])
            colors.extend(wall_color)
        if self.flags[0]:  # Left
            vertices.extend([x1, y2, x1, y1])
            colors.extend(wall_color)

        if vertices:
            self.lines = lines_batch.add(len(vertices) // 2, GL_LINES, OrderedGroup(1),
                ('v2f', vertices),
                ('c3B', colors))