# visual_grid_game.py

import random
import tkinter as tk

class VisualGridHuntGame:
    """A flexible Pacman-style grid environment with support for configurable opponents and larger scales."""

    def __init__(self, width=10, height=10, num_food=10, num_opponents=2, num_traps=5, custom_walls=None):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)
        
        # --- ADDED THIS LINE FOR PARTIAL OBSERVABILITY ---
        self.agent_facing = 'Right'  # Tracks facing direction: 'Up', 'Down', 'Left', 'Right'

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        self.food_positions = set()
        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)
            if (fx, fy) != (0, 0) and (fx, fy) not in self.walls:
                self.food_positions.add((fx, fy))

        self.toxic_traps = set()
        while len(self.toxic_traps) < num_traps:
            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)
            if (tx, ty) != (0, 0) and (tx, ty) not in self.walls and (tx, ty) not in self.food_positions:
                self.toxic_traps.add((tx, ty))

        self.opponents = []
        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)
            if (ox, oy) != (0, 0) and (ox, oy) not in self.walls and (ox, oy) not in self.food_positions:
                self.opponents.append([ox, oy])

        self.score = 0
        self.steps = 0
        self.collision = False

    # --- REPLACE YOUR OLD get_percept METHOD WITH THIS ONE ---
    def get_percept(self) -> dict:
        """Step 1.1: Returns local sensory booleans instead of global agent coordinates."""
        x, y = self.agent_pos

        # Determine cell coordinates directly ahead of agent's current orientation
        ahead_x, ahead_y = x, y
        if self.agent_facing == 'Up':
            ahead_y += 1
        elif self.agent_facing == 'Down':
            ahead_y -= 1
        elif self.agent_facing == 'Left':
            ahead_x -= 1
        elif self.agent_facing == 'Right':
            ahead_x += 1

        # Check if the target cell ahead is off-grid or inside a wall
        out_of_bounds = not (0 <= ahead_x < self.width and 0 <= ahead_y < self.height)
        is_wall = (ahead_x, ahead_y) in self.walls

        return {
            'food_here': tuple(self.agent_pos) in self.food_positions,
            'wall_ahead': is_wall or out_of_bounds,
            'smells_toxin': tuple(self.agent_pos) in self.toxic_traps,
        }

    def execute_action(self, action: str):
        self.steps += 1
        
        # --- UPDATE FACING DIRECTION WHEN MOVING ---
        self.agent_facing = action
        
        new_pos = list(self.agent_pos)

        if action == 'Up':
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right':
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        if tuple(new_pos) in self.walls:
            self.score -= 5
        else:
            self.agent_pos = new_pos

        tuple_pos = tuple(self.agent_pos)
        if tuple_pos in self.food_positions:
            self.food_positions.remove(tuple_pos)
            self.score += 20

        if tuple_pos in self.toxic_traps:
            self.score -= 15

        for op in self.opponents:
            move = random.choice(['Up', 'Down', 'Left', 'Right', 'Stay'])
            if move == 'Up' and op[1] < self.height - 1:
                op[1] += 1
            elif move == 'Down' and op[1] > 0:
                op[1] -= 1
            elif move == 'Left' and op[0] > 0:
                op[0] -= 1
            elif move == 'Right' and op[0] < self.width - 1:
                op[0] += 1

            if op == self.agent_pos:
                self.score -= 50
                self.collision = True

    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 60 or self.collision