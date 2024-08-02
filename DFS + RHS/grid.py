import pyglet
from cell import Cell
from colors import *
from test import RightHandSolver
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


        self.solving = False
        self.solver = None
        self.start_cell = self.grid[self.rows-1]
        self.end_cell = self.grid[-1]

        pyglet.clock.schedule_interval(self.update, 1/120.0)  # Update 30 times per second
    
    def setup(self):
        for j in range(self.columns):
            for i in range(self.rows):
                cell = Cell(i, j)
                cell.cols = self.rows
                cell.rows = self.columns
                cell.show(self.cell_size, self.cell_batch, self.lines_batch,  self.color_manager.colors['walls'])
                self.grid.append(cell)
        
        self.current = self.grid[0]  # Start with the first cell
        self.current.visited = True

    def update_visited_colors(self):
        """Update the color of visited cells based on the transition."""
        visited_color = self.color_manager.get_visited_color()
        for cell in self.grid:
            if cell.visited:
                cell.fill_color = visited_color

    def update(self, dt):
        if not self.solving: 
            self.color_manager.update(dt)
            self.update_visited_colors()     # Update colors of visited cells

            next_cell = self.current.checkNeighbours(self.grid)
            self.current.fill_color = self.color_manager.colors['current']  # Color for current cell

            if next_cell:
                next_cell.visited = True
                self.stack.append(self.current)
                self.removeWalls(self.current, next_cell)
                self.current = next_cell
            elif len(self.stack) > 0:
                self.current = self.stack.pop()

            else:
                self.solving = True
                self.solver = RightHandSolver(self.start_cell, self.end_cell, self.grid,self.rows, self.columns)
                for cell in self.grid:
                    cell.visited = False
                print("Maze generation complete. Starting to solve.")
        else:
            if not self.solver.finished:
                current, next_cell = self.solver.step()
                # print(f"curr : {current.x},{current.y},next : {next_cell.x},{next_cell.y}")
                if current:
                    current.fill_color = self.color_manager.colors['solving']
                if next_cell:
                    
                    if next_cell.visited == True:
                        
                        current.fill_color = self.color_manager.colors['backtrack']
                        
                    
                    next_cell.fill_color = self.color_manager.colors['current']
            else:
                self.solver.path = [cell for cell in  self.solver.path if cell.fill_color != (128,128,128)]

                for cell in self.solver.path:

                    cell.fill_color = self.color_manager.colors['path']
                    
            
        for cell in self.grid:
            cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.color_manager.colors['walls'])

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