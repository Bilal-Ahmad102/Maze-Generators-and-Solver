import pyglet
from cell import Cell
from colors import *
import random
class MazeGrid:
    def __init__(self):
        self.window = pyglet.window.Window(450, 650, "Maze Grid")
        self.cell_size = 25
        self.rows = int(self.window.width / self.cell_size)
        self.columns = int(self.window.height / self.cell_size)
        self.grid = []
        self.stack = []
        self.current = None

        self.color_manager = ColorManager()

        self.cell_batch = pyglet.graphics.Batch()
        self.lines_batch = pyglet.graphics.Batch()
        self.setup()
        self.window.push_handlers(on_draw=self.on_draw)

        pyglet.clock.schedule_interval(self.update, 1/60.0)  # Update 30 times per second
    
    def setup(self):
        for j in range(self.columns):
            for i in range(self.rows):
                cell = Cell(i, j)
                cell.cols = self.rows
                cell.rows = self.columns
                cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])
                self.grid.append(cell)
        
        self.current = self.grid[random.randint(0,len(self.grid))]  # Start with the first cell
        self.current.visited = True

    def update_visited_colors(self):
        """Update the color of visited cells based on the transition."""
        visited_color = self.color_manager.get_visited_color()
        for cell in self.grid:
            if cell.visited:
                cell.fill_color = visited_color

    def update(self, dt):
        self.color_manager.update(dt)
        self.update_visited_colors()

        if not all(cell.visited for cell in self.grid):
            # Color the current cell white
            self.current.fill_color = self.color_manager.colors['current']

            neighbors = self.current.checkNeighbours(self.grid)
            if isinstance(neighbors, Cell):  # If only one neighbor is returned
                neighbors = [neighbors]
            if neighbors:
                next_cell = random.choice(neighbors)
                if not next_cell.visited:
                    self.removeWalls(self.current, next_cell)
                    next_cell.visited = True
                self.current = next_cell
        else:
            # Maze is complete
            pass

        for cell in self.grid:
            if cell == self.current:
                cell.fill_color = self.color_manager.colors['current']
            cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])

    def removeWalls(self, a, b):
        x = a.x - b.x
        if x == -1:
            a.flags[2] = False
            b.flags[0] = False 
        elif x == 1:
            a.flags[0] = False
            b.flags[2] = False 
        y = a.y - b.y
        if y == -1:
            a.flags[1] = False
            b.flags[3] = False 
        if y == 1:
            a.flags[3] = False
            b.flags[1] = False 
            
    def on_draw(self):
        self.window.clear()
        self.cell_batch.draw()
        self.lines_batch.draw()

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    maze = MazeGrid()
    maze.run()