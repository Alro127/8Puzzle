import tkinter as tk
from tkinter import ttk, messagebox
import os
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

# Algorithms

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


def dfs(start_state):
    start = Puzzle(start_state)
    visited = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current.is_goal():
            return current.get_path()
        visited.add(current.to_tuple())
        for neighbor in current.get_neighbors():
            if neighbor.to_tuple() not in visited:
                stack.append(neighbor)
    return []

# Visualization

def visualize_puzzle(state, step, output_dir):
    plt.figure(figsize=(4, 4))
    plt.imshow([[1 if cell == 0 else 0 for cell in row] for row in state], cmap='gray', vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(state[i][j]), ha='center', va='center', fontsize=16, color='red')
    plt.title(f"Step: {step}")
    plt.axis('off')
    plt.savefig(os.path.join(output_dir, f"frame_{step}.png"))
    plt.close()


def create_gif(frames, output_filename):
    images = [Image.open(frame) for frame in frames]
    images[0].save(output_filename, save_all=True, append_images=images[1:], duration=300, loop=0)


def generate_gif(start_state, algorithm, output_filename):
    output_dir = algorithm
    os.makedirs(output_dir, exist_ok=True)

    if algorithm == 'BFS':
        path = bfs(start_state)
    elif algorithm == 'DFS':
        path = dfs(start_state)
    else:
        messagebox.showerror("Error", "Unknown algorithm selected.")
        return

    frames = []
    for step, state in enumerate(path):
        visualize_puzzle(state, step, output_dir)
        frames.append(os.path.join(output_dir, f"frame_{step}.png"))

    create_gif(frames, os.path.join(output_dir, output_filename))


# GUI

class PuzzleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Solver GUI")
        self.root.geometry("400x400")

        self.board = []
        self.create_board()

        self.algorithm_label = tk.Label(root, text="Algorithm:")
        self.algorithm_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        self.algorithm_combo = ttk.Combobox(root, values=["BFS", "DFS"], state="readonly")
        self.algorithm_combo.current(0)
        self.algorithm_combo.grid(row=5, column=0, columnspan=3)

        self.generate_button = tk.Button(root, text="Generate GIF", command=self.generate_gif)
        self.generate_button.grid(row=6, column=0, columnspan=3, pady=(10, 0))

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                entry = tk.Entry(self.root, width=3, font=('Arial', 24), justify='center')
                entry.insert(0, '0')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.board.append(row)

    def generate_gif(self):
        try:
            start_state = [[int(self.board[i][j].get()) for j in range(3)] for i in range(3)]
            algorithm = self.algorithm_combo.get()
            generate_gif(start_state, algorithm, "output.gif")
            messagebox.showinfo("Success", f"GIF created in {algorithm}/output.gif")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PuzzleSolverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()