import pyglet
from cell import Cell
from colors import *
import random
from test import AStar

class MazeGrid:
    def __init__(self):
        self.window = pyglet.window.Window(450, 650, "Maze Grid")
        self.cell_size = 25
        self.rows = int(self.window.width / self.cell_size)
        self.columns = int(self.window.height / self.cell_size)
        self.grid = []
        self.walls = []
        self.current_cells = []

        self.color_manager = ColorManager()

        self.cell_batch = pyglet.graphics.Batch()
        self.lines_batch = pyglet.graphics.Batch()
        self.setup()
        self.window.push_handlers(on_draw=self.on_draw)

        self.maze_generated = False
        self.astar = None
        self.start_cell = None
        self.end_cell = None
        self.astar_finished = False

        self.open_set_cells = set()
        self.closed_set_cells = set()
        self.path_cells = set()

        pyglet.clock.schedule_interval(self.update, 1/30.0)  # Update 30 times per second
    
    # ... [keep other methods as they were] ...

    def update(self, dt):
        self.color_manager.update(dt)

        if not self.maze_generated:
            steps_per_update = 10  # Reduced for better visualization

            for _ in range(steps_per_update):
                if self.walls:
                    cell1, cell2, wall = self.walls.pop()
                    if not cell2.visited:
                        self.current_cells = [cell1, cell2]
                        self.remove_walls(cell1, cell2, wall)
                        cell2.visited = True
                        self.add_walls(cell2)
                        random.shuffle(self.walls)
                    else:
                        self.current_cells = []
                else:
                    # Maze is complete
                    self.current_cells = []
                    self.maze_generated = True
                    self.start_a_star()
                    break
        elif self.astar and not self.astar_finished:
            if self.astar.step():
                # A* has finished
                self.astar_finished = True
                self.path_cells = set(self.astar.path)

        self.update_colors()

        for cell in self.grid:
            cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])

    def start_a_star(self):
        self.start_cell = self.grid[0]  # Top-left cell
        self.end_cell = self.grid[-1]  # Bottom-right cell
        self.astar = AStar(self.grid, self.start_cell, self.end_cell)

    def update_colors(self):
        """Update the color of cells based on their state."""
        visited_color = self.color_manager.get_visited_color()
        for cell in self.grid:
            if cell in self.current_cells:
                cell.fill_color = self.color_manager.colors['current']
            elif cell.visited:
                cell.fill_color = visited_color
            else:
                cell.fill_color = self.color_manager.colors['unvisited']

        if self.astar:
            # Update open and closed sets
            self.open_set_cells = set(item[2] for item in self.astar.open_set)
            self.closed_set_cells = set(self.astar.came_from.keys()) - self.open_set_cells

            for cell in self.open_set_cells:
                cell.fill_color = (0, 255, 0)  # Green for open set
            for cell in self.closed_set_cells:
                cell.fill_color = (200, 200, 200)  # Light gray for closed set
            if self.astar.current:
                self.astar.current.fill_color = (255, 255, 255)  # Yellow for current cell

        # Always color the path and start/end cells last to ensure they're visible
        for cell in self.path_cells:
            cell.fill_color = (0, 0, 255)  # Blue for the path

        if self.start_cell:
            self.start_cell.fill_color = (0, 255, 0)  # Green for start
        if self.end_cell:
            self.end_cell.fill_color = (255, 0, 0)  # Red for end

    
    def setup(self):
        for j in range(self.columns):
            for i in range(self.rows):
                cell = Cell(i, j)
                cell.cols = self.rows
                cell.rows = self.columns
                cell.show(self.cell_size, self.cell_batch, self.lines_batch, self.columns-1, self.color_manager.colors['walls'])
                cell.fill_color = self.color_manager.colors['unvisited']
                self.grid.append(cell)
        
        # Start with a random cell
        start_cell = random.choice(self.grid)
        start_cell.visited = True

        # Add all neighboring walls of the start cell to the list
        self.add_walls(start_cell)
        random.shuffle(self.walls)

    def add_walls(self, cell):
        x, y = cell.x, cell.y
        if x < self.rows - 1:
            self.walls.append((cell, self.grid[x + 1 + y * self.rows], 2))  # Right wall
        if y < self.columns - 1:
            self.walls.append((cell, self.grid[x + (y + 1) * self.rows], 1))  # Bottom wall
        if x > 0:
            self.walls.append((cell, self.grid[x - 1 + y * self.rows], 0))  # Left wall
        if y > 0:
            self.walls.append((cell, self.grid[x + (y - 1) * self.rows], 3))  # Top wall


    def remove_walls(self, a, b, wall):
        if wall == 2:  # Right wall
            a.flags[2] = False
            b.flags[0] = False
        elif wall == 1:  # Bottom wall
            a.flags[1] = False
            b.flags[3] = False
        elif wall == 0:  # Left wall
            a.flags[0] = False
            b.flags[2] = False
        elif wall == 3:  # Top wall
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