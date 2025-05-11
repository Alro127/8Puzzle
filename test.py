import copy
import matplotlib.pyplot as plt
from PIL import Image

class Puzzle:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state  
        self.parent = parent
        self.move = move
        self.depth = depth
        self.blank_pos = self.find_blank()

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
                
    def get_neighbors(self):
        neighbors = []
        bi, bj = self.blank_pos
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = copy.deepcopy(self.state)
                new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
                neighbors.append(Puzzle(new_state, parent=self, move=(ni, nj), depth=self.depth + 1))
        return neighbors
    
    def is_goal(self):
        return self.state == [[1,2,3],[4,5,6],[7,8,0]]

    def to_tuple(self):
        return tuple(tuple(row) for row in self.state)
    
    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

def bfs(start_state):
    start = Puzzle(start_state)
    visited = set()
    queue = [start]
    while queue:
        current = queue.pop(0)
        if current.is_goal():
            return current.get_path()
        
        visited.add(current.to_tuple())
        for neighbor in current.get_neighbors():
            if neighbor.to_tuple() not in visited:
                queue.append(neighbor)

    return []

def visualize_puzzle(state, step):
    plt.figure(figsize=(4, 4))
    plt.imshow([[1 if cell == 0 else 0 for cell in row] for row in state], cmap='gray', vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(state[i][j]), ha='center', va='center', fontsize=16, color='red')
    plt.title(f"Step: {step}")
    plt.axis('off')
    plt.savefig(f"frame_{step}.png")
    plt.close()

def create_gif(frames, output_filename):
    images = [Image.open(frame) for frame in frames]
    images[0].save(output_filename, save_all=True, append_images=images[1:], duration=300, loop=0)

def main():
    start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    path = bfs(start_state)

    frames = []
    for step, state in enumerate(path):
        visualize_puzzle(state, step)
        frames.append(f"frame_{step}.png")

    create_gif(frames, "puzzle_solution.gif")

main()
