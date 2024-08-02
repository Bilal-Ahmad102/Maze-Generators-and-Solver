import pyglet
from cell import Cell
from colors import *
import random
from test import Dijkstra

class MazeGrid:
    def __init__(self):
        self.window = pyglet.window.Window(450, 650, "Maze Grid")
        self.cell_size = 50
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

        self.maze_generated = False
        self.dijkstra = None
        self.start_cell = None
        self.end_cell = None

        pyglet.clock.schedule_interval(self.update, 1/90.0)  # Update 30 times per second
    
    def setup(self):
        for j in range(self.columns):
            for i in range(self.rows):
                cell = Cell(i, j)
                cell.cols = self.rows
                cell.rows = self.columns
                cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])
                self.grid.append(cell)
        
        self.current = self.grid[0]  # Start with the first cell
        self.current.visited = True

    def update_visited_colors(self):
        visited_color = self.color_manager.get_visited_color()
        for cell in self.grid:
            if cell.visited:
                cell.fill_color = visited_color

    def update(self, dt):
        self.color_manager.update(dt)
        self.update_visited_colors()

        if not self.maze_generated:
            self.generate_maze_step()
        elif self.dijkstra is None:
            self.start_dijkstra()
            
        elif not self.dijkstra.finished:
            self.dijkstra_step()

        else:
            self.highlight_path()

        
        for cell in self.grid:
            cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])

    def dijkstra_step(self):
        self.dijkstra.step()
        if self.dijkstra.current:
            self.dijkstra.current.fill_color = (0, 255, 0)  # Green for visited cells
            self.dijkstra.current.visited = True
    
        if self.dijkstra.finished:
            self.highlight_path()
    
    def unvisite_cells(self):
        for cell in self.grid:
            cell.visited =False
            
    def highlight_path(self):
        for cell in self.dijkstra.path:
            cell.fill_color = (255, 255, 0)  # Yellow for the shortest path

    def generate_maze_step(self):
        self.current.fill_color = self.color_manager.colors['current']

        neighbors = self.current.checkNeighbours(self.grid)
        unvisited_neighbors = [n for n in neighbors if not n.visited]

        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            self.removeWalls(self.current, next_cell)
            next_cell.visited = True
            self.stack.append(self.current)
            self.current = next_cell
        elif self.stack:
            self.current = self.stack.pop()
        else:
            self.maze_generated = True

    def start_dijkstra(self):
        self.start_cell = self.grid[0]
        self.end_cell = self.grid[-1]
        self.dijkstra = Dijkstra(self.grid, self.start_cell, self.end_cell)
        self.unvisite_cells()
        
    def dijkstra_step(self):
        self.dijkstra.step()
        if self.dijkstra.current:
            self.dijkstra.current.fill_color = (0, 255, 0)  # Green for visited cells

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