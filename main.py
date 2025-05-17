import tkinter as tk
from tkinter import ttk, messagebox
import tracemalloc, timeit
from PIL import Image
import os
import matplotlib.pyplot as plt
from ObservableEnvironmet import bfs, dfs, dls, ucs, ids, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing, beam_search, genetic_algorithm
from And_OrSearch import and_or_search_solution
from Backtracking import backtracking_solve, backtracking_solve_with_forward_checking
from Fill_CSP import backtracking_fill, forward_checking_fill, min_conflict_fill
from PartiallyObservable import bfs_partially_observable
from NoObservable import bfs_no_observable
from ReinforcementLearning import QLearningSolver

class PuzzleSolverGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8 Puzzle Solver - AI Algorithm Visualizer")
        self.configure(bg="#1F1F1F")
        self.geometry("900x600")

        # Left Frame for Puzzle Display
        self.left_frame = tk.Frame(self, width=410, height=450, bg="#1F1F1F", bd=2, relief="ridge", highlightthickness=2, highlightbackground="#61AFEF")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        self.left_frame.grid_propagate(False)

        # Right Frame for Algorithm Selection
        self.right_frame = tk.Frame(self, width=330, height=600, bg="#1F1F1F", bd=0, highlightthickness=0)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)
        self.right_frame.grid_propagate(False)

        # Dropdown Menu for Algorithms
        self.algorithm_label = tk.Label(self.right_frame, text="Thuật Toán:", fg="#61AFEF", bg="#2C2C2C", font=("Helvetica", 14, "bold"))
        self.algorithm_label.pack(pady=(20, 10))
        self.algorithm_options = ["BFS", "DFS", "DLS", "UCS", "IDS", "Greedy", "A Start", "IDA Start", "Simple Hill Climbing", "Steepest Ascent", "Stochastic", "Simulated Annealing", "Beam Search", "Genetic Algorithm", "And Or Search", "No Observable" ,"Partially Observable", "Backtracking", "Backtracking with Forward Checking", "Fill Backtracking", "Fill Backtracking with Forward Checking", "Min Conflict", "And Or Search", "Q Learning"]
        self.algorithm_var = tk.StringVar()
        self.algorithm_menu = ttk.Combobox(self.right_frame, textvariable=self.algorithm_var, values=self.algorithm_options)
        self.algorithm_menu.pack(pady=10, fill="x", padx=20)
        self.algorithm_menu.configure(background="#3E4451", foreground="#61AFEF", font=("Helvetica", 12))
        self.algorithm_menu.configure(background="#61AFEF", foreground="#282C34")

        # Buttons
        self.randomize_button = tk.Button(self.right_frame, text="Tạo trạng thái phức tạp", command=self.initial_puzzle, bg="#61AFEF", fg="#282C34", font=("Helvetica", 10, "bold"))
        self.randomize_button.pack(pady=10, fill="x", padx=20)
        self.randomize_simple_button = tk.Button(self.right_frame, text="Tạo trạng thái đơn giản", command=self.simple_initial_puzzle, bg="#61AFEF", fg="#282C34", font=("Helvetica", 10, "bold"))
        self.randomize_simple_button.pack(pady=10, fill="x", padx=20)
        self.start_button = tk.Button(self.right_frame, text="Bắt đầu giải", command=self.solve_puzzle, bg="#98C379", fg="#282C34", font=("Helvetica", 10, "bold"))
        self.start_button.pack(pady=10, fill="x", padx=20)

        self.export_button = tk.Button(self.right_frame, text="Xuất GIF", command=self.export_gif, bg="#E06C75", fg="#282C34", font=("Helvetica", 10, "bold"))
        self.export_button.pack(pady=10, fill="x", padx=20)

        # Initial Puzzle State
        self.puzzle_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        self.path = []
        self.draw_puzzle()

    def initial_puzzle(self):
        self.puzzle_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        self.draw_puzzle()

    def simple_initial_puzzle(self):
        self.puzzle_state = [[1, 2, 3], [0, 4, 5], [7, 8, 6]]
        self.draw_puzzle()

    def move_tile(self, i, j):
        bi, bj = [(x, y) for x in range(3) for y in range(3) if self.puzzle_state[x][y] == 0][0]
        if (abs(bi - i) == 1 and bj == j) or (abs(bj - j) == 1 and bi == i):
            self.puzzle_state[bi][bj], self.puzzle_state[i][j] = self.puzzle_state[i][j], self.puzzle_state[bi][bj]
            self.draw_puzzle()

    def draw_puzzle(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for i, row in enumerate(self.puzzle_state):
            for j, val in enumerate(row):
                tile = tk.Button(self.left_frame, text=str(val), font=("Helvetica", 24, "bold"), width=6, height=3, borderwidth=1, relief="raised", command=lambda i=i, j=j: self.move_tile(i, j), bg="#61AFEF" if val != 0 else "#1F1F1F", fg="#1F1F1F" if val != 0 else "#61AFEF")
                tile.grid(row=i, column=j, padx=5, pady=5)

    def visualize_puzzle(self, state, step, output_dir): 
        plt.figure(figsize=(4, 4))
        
        # Sử dụng nền trắng và ô trống màu sáng
        plt.imshow([[1 if cell == 0 else 0.8 for cell in row] for row in state], cmap='Blues', vmin=0, vmax=1)
        
        # Đặt số với màu đen và có độ đậm
        for i in range(3):
            for j in range(3):
                plt.text(j, i, str(state[i][j]), ha='center', va='center', fontsize=16, color='white', fontweight='bold')
        
        plt.title(f"Step: {step}", fontsize=18, fontweight='bold', color='black')
        plt.axis('off')
        
        # Lưu hình ảnh với tên file phù hợp
        plt.savefig(os.path.join(output_dir, f"frame_{step}.png"))
        plt.close()


    def create_gif(self, frames, output_filename):
        images = [Image.open(frame) for frame in frames]
        images[0].save(output_filename, save_all=True, append_images=images[1:], duration=300, loop=0)

    def generate_gif(self, algorithm, output_filename):
        output_dir = algorithm
        os.makedirs(output_dir, exist_ok=True)

        frames = []
        for step, state in enumerate(self.path):
            self.visualize_puzzle(state, step, output_dir)
            frames.append(os.path.join(output_dir, f"frame_{step}.png"))

        self.create_gif(frames, os.path.join(output_dir, output_filename))

    def solve_puzzle(self):
        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showwarning("Lỗi", "Vui lòng chọn thuật toán")
            return

        self.path = []
        tracemalloc.start()
        start_time = timeit.default_timer()

        if algorithm == 'BFS':
            self.path = bfs(self.puzzle_state)
        elif algorithm == 'DFS':
            self.path = dfs(self.puzzle_state)
        elif algorithm == 'DLS':
            self.path = dls(self.puzzle_state)
        elif algorithm == 'UCS':
            self.path = ucs(self.puzzle_state)
        elif algorithm == 'IDS':
            self.path = ids(self.puzzle_state)
        elif algorithm == 'Greedy':
            self.path = greedy(self.puzzle_state)
        elif algorithm == 'A Start':
            self.path = astar(self.puzzle_state)
        elif algorithm == 'IDA Start':
            self.path = ida_star(self.puzzle_state)
        elif algorithm == 'Simple Hill Climbing':
            self.path = simple_hill_climbing(self.puzzle_state)
        elif algorithm == 'Steepest Ascent':
            self.path = steepest_ascent_hill_climbing(self.puzzle_state)
        elif algorithm == 'Stochastic':
            self.path = stochastic_hill_climbing(self.puzzle_state)
        elif algorithm == 'Simulated Annealing':
            self.path = simulated_annealing(self.puzzle_state)
        elif algorithm == 'Beam Search':
            self.path = beam_search(self.puzzle_state)
        elif algorithm == 'Genetic Algorithm':
            self.path = genetic_algorithm(self.puzzle_state)
        elif algorithm == 'No Observable':
            self.path = bfs_no_observable(self.puzzle_state)
        elif algorithm == 'Partially Observable':
            self.path = bfs_partially_observable(self.puzzle_state)
        elif algorithm == 'Backtracking':
            self.path = backtracking_solve(self.puzzle_state)
        elif algorithm == 'Backtracking with Forward Checking':
            self.path = backtracking_solve_with_forward_checking(self.puzzle_state)
        elif algorithm == 'Fill Backtracking':
            self.puzzle_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            self.path = backtracking_fill(self.puzzle_state)
        elif algorithm == 'Fill Backtracking with Forward Checking':
            self.puzzle_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            self.path = forward_checking_fill(self.puzzle_state)
        elif algorithm == 'Min Conflict':
            self.puzzle_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            self.path = min_conflict_fill(self.puzzle_state)
        elif algorithm == 'And Or Search':
            self.path = and_or_search_solution(self.puzzle_state)
        elif algorithm == 'Q Learning':
            q_solver = QLearningSolver()
            q_solver.train(self.puzzle_state, episodes=500)
            self.path = q_solver.get_solution_path(self.puzzle_state)
        else:
            messagebox.showerror("Error", "Thuật toán không được hỗ trợ")
            return
        
        end_time = timeit.default_timer()
        memory_used, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Thời gian thực thi thuật toán: {(end_time - start_time):.5f} giây")
        print(f"Bộ nhớ sử dụng: {memory_used / (1024 ** 2):.5f} MB")
        print(f"Bộ nhớ tối đa: {peak_memory / (1024 ** 2):.5f} MB")
        

        if self.path == []:
            messagebox.showinfo("Info", "Không tìm được lời giải")
        else:
            print("Số bước thực hiện:", len(self.path))
            for state in self.path:
                self.puzzle_state = state
                self.draw_puzzle()
                self.update()
                self.after(300)

    def export_gif(self):
        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showwarning("Lỗi", "Vui lòng chọn thuật toán")
            return
        self.generate_gif(algorithm, f"{algorithm}_solution.gif")
        messagebox.showinfo("Thông báo", f"GIF đã được xuất thành công: {algorithm}_solution.gif")

if __name__ == "__main__":
    app = PuzzleSolverGUI()
    app.mainloop()
