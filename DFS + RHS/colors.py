class ColorManager:
    def __init__(self):
        self.start_color = (0, 255, 255)  # Cyan
        self.end_color = (255, 0, 255)    # Magenta
        self.color_change_duration = 5  # Duration in seconds for a full transition
        self.color_timer = 0  # Start at 0 for initial transition

        self.colors = {
            'unvisited': (0, 0, 0),  # Black for unvisited cells
            'current': (255, 255, 255),  # White for current cell
            'walls': [0,0, 0, 0, 0, 0],  # Default walls color
            'solving':(0, 255, 255),
            'path':(0,0,255),
            'backtrack':(128,128,128)
            
        }

    def interpolate_color(self, start_color, end_color, t):
        """Interpolate between start_color and end_color by t (0.0 to 1.0)."""
        return (
            int(start_color[0] + (end_color[0] - start_color[0]) * t),
            int(start_color[1] + (end_color[1] - start_color[1]) * t),
            int(start_color[2] + (end_color[2] - start_color[2]) * t)
        )

    def get_visited_color(self):
        """Get the current color for visited cells."""
        t = (self.color_timer % self.color_change_duration) / self.color_change_duration
        if int(self.color_timer / self.color_change_duration) % 2 == 1:
            t = 1 - t  # Reverse the interpolation for odd cycles
        return self.interpolate_color(self.start_color, self.end_color, t)

    def update(self, dt):
        """Update the color timer."""
        self.color_timer += dt








color_combinations = {
    'combination_1': {
        'visited': (173, 216, 230),  # Light Blue
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (0, 255, 255),  # Cyan
        'walls_color': [255, 0, 255, 255, 0, 255]  # Magenta
    },
    'combination_2': {
        'visited': (255, 255, 0),  # Yellow
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (50, 205, 50),  # Lime Green
        'walls_color': [255, 165, 0, 255, 165, 0]  # Orange
    },
    'combination_3': {
        'visited': (255, 20, 147),  # Deep Pink
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (0, 191, 255),  # Deep Sky Blue
        'walls_color': [255, 69, 0, 255, 69, 0]  # Red-Orange
    },
    'combination_4': {
        'visited': (255, 182, 193),  # Light Pink
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (124, 252, 0),  # Lawn Green
        'walls_color': [255, 0, 0, 255, 0, 0]  # Bright Red
    },
    'combination_5': {
        'visited': (135, 206, 250),  # Light Sky Blue
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (0, 255, 127),  # Spring Green
        'walls_color': [238, 130, 238, 238, 130, 238]  # Violet
    },
    'combination_6': {
        'visited': (255, 140, 0),  # Dark Orange
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (255, 105, 180),  # Hot Pink
        'walls_color': [0, 255, 0, 0, 255, 0]  # Bright Green
    },
    'combination_7': {
        'visited': (147, 112, 219),  # Medium Purple
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (0, 255, 255),  # Aqua
        'walls_color': [255, 20, 147, 255, 20, 147]  # Deep Pink
    },
    'combination_8': {
        'visited': (0, 191, 255),  # Deep Sky Blue
        'unvisited': (0, 0, 0),  # Black
        'fill_color': (255, 165, 0),  # Orange
        'walls_color': [255, 0, 255, 255, 0, 255]  # Magenta
    }
}
