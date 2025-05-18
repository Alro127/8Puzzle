import copy
import random
from collections import deque

class Puzzle:
    def __init__(self, state, parent=None, move=None, depth=0, node_id=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.blank_pos = self.find_blank()
        parent_id = parent.node_id if parent else "root"
        self.node_id = node_id if node_id else f"{parent_id}_{str(id(self))}_{depth}"

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def get_neighbors(self):
        neighbors = []
        bi, bj = self.blank_pos
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = copy.deepcopy(self.state)
                new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
                neighbors.append(Puzzle(new_state, parent=self, move=(ni, nj), depth=self.depth + 1))
        return neighbors

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def heuristic(self):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_i, goal_j = divmod(value - 1, 3)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def to_tuple(self):
        return tuple(tuple(row) for row in self.state)

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()


def generate_belief_states(state, num_beliefs=1):
    beliefs = [state]
    for _ in range(num_beliefs):
        new_state = copy.deepcopy(state)
        bi, bj = random.randint(0, 2), random.randint(0, 2)
        ni, nj = random.randint(0, 2), random.randint(0, 2)
        new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
        beliefs.append(new_state)
    return beliefs


def bfs_no_observable(start_state, num_beliefs=1):
    initial_beliefs = generate_belief_states(start_state, num_beliefs)
    queue = deque()
    visited = set()

    for belief_state in initial_beliefs:
        initial_node = Puzzle(belief_state)
        queue.append(initial_node)
        visited.add(initial_node)

    while queue:
        current = queue.popleft()
        neighbors = current.get_neighbors()

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                if neighbor.is_goal():
                    return [n.state for n in neighbor.get_path()]
                queue.append(neighbor)

    return []