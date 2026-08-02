# agent.py
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """Step 1.2: Memoryless agent using Condition-Action IF-THEN rules."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # Rule 1: IF food_here THEN act
        if percept.get('food_here', False):
            return 'Up'

        # Rule 2: IF wall_ahead THEN turn right
        if percept.get('wall_ahead', False):
            return 'Right'

        # Default action
        return 'Up'


class ModelBasedAgent:
    """Step 1.3: Agent maintaining internal memory to track state and escape loops."""

    def __init__(self):
        self.visited_cells = set()
        self.current_pos = (0, 0)
        self.last_action = None
        self.directions = ['Up', 'Right', 'Down', 'Left']

    def sense_and_act(self, percept: dict) -> str:
        # 1. Update Transition Model
        if self.last_action == 'Up':
            self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)
        elif self.last_action == 'Down':
            self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
        elif self.last_action == 'Left':
            self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
        elif self.last_action == 'Right':
            self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])

        # 2. Update Sensor Model / Memory
        self.visited_cells.add(self.current_pos)

        # 3. Condition-Action Rules querying Memory
        if percept.get('wall_ahead', False):
            choices = ['Down', 'Left', 'Right', 'Up']
            random.shuffle(choices)
            selected_action = choices[0]
            self.last_action = selected_action
            return selected_action

        selected_action = random.choice(self.directions)
        self.last_action = selected_action
        return selected_action


class SearchAgent:
    """Practical 3: SearchAgent implementing BFS pathfinding."""

    def bfs_search(self, start, goal, walls, grid_size):
        from collections import deque

        width, height = grid_size
        walls_set = set(walls)

        queue = deque([(start, [])])
        visited = {start}

        moves = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0),
        }

        while queue:
            curr_pos, path = queue.popleft()

            if curr_pos == goal:
                return path

            for action, (dx, dy) in moves.items():
                next_pos = (curr_pos[0] + dx, curr_pos[1] + dy)

                if (
                    0 <= next_pos[0] < width
                    and 0 <= next_pos[1] < height
                    and next_pos not in walls_set
                    and next_pos not in visited
                ):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return None