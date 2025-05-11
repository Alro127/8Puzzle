import numpy as np
import random
from collections import defaultdict

class Puzzle:
    def __init__(self, state):
        self.state = state
        self.blank_pos = self.find_blank()

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def get_actions(self):
        actions = []
        bi, bj = self.blank_pos
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                actions.append((di, dj))
        return actions

    def move(self, action):
        bi, bj = self.blank_pos
        ni, nj = bi + action[0], bj + action[1]
        new_state = [row[:] for row in self.state]
        new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
        return Puzzle(new_state)

    def to_tuple(self):
        return tuple(tuple(row) for row in self.state)

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def calculate_manhattan_distance(self):
        goal = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_x, goal_y = goal[value]
                    distance += abs(goal_x - i) + abs(goal_y - j)
        return distance

class QLearningSolver:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.visited_states = set()

    def choose_action(self, state, actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(actions)
        q_values = {action: self.q_table[state][action] for action in actions}
        max_q = max(q_values.values(), default=0)
        max_actions = [action for action, q in q_values.items() if q == max_q]
        return random.choice(max_actions)

    def update_q(self, state, action, reward, next_state, next_actions):
        current_q = self.q_table[state][action]
        max_next_q = max([self.q_table[next_state][a] for a in next_actions], default=0)
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q - current_q)

    def train(self, state, episodes=500):
        puzzle = Puzzle(state)
        for episode in range(episodes):
            state = puzzle.to_tuple()
            steps = 0
            while not puzzle.is_goal() and steps < 50:
                actions = puzzle.get_actions()
                action = self.choose_action(state, actions)
                next_puzzle = puzzle.move(action)
                next_state = next_puzzle.to_tuple()

                # Tính toán khoảng cách Manhattan một lần
                current_distance = puzzle.calculate_manhattan_distance()
                next_distance = next_puzzle.calculate_manhattan_distance()

                # Cải tiến hệ thống thưởng: Tính điểm linh hoạt
                if next_puzzle.is_goal():
                    reward = 100  # Nếu đạt được mục tiêu, thưởng điểm tối đa
                elif next_distance < current_distance:
                    # Nếu khoảng cách Manhattan giảm, thưởng nhiều hơn
                    reward = 20 + (current_distance - next_distance) * 2
                elif next_distance == current_distance:
                    # Nếu không thay đổi, phạt nhẹ
                    reward = -2
                else:
                    # Nếu khoảng cách tăng lên, phạt nặng hơn
                    reward = -10

                # Cập nhật Q-value
                next_actions = next_puzzle.get_actions()
                self.update_q(state, action, reward, next_state, next_actions)

                # Theo dõi các trạng thái đã thăm
                self.visited_states.add(next_state)

                # Di chuyển đến trạng thái tiếp theo
                puzzle = next_puzzle
                state = next_state
                steps += 1

            # Giảm epsilon một cách linh hoạt dựa trên hiệu suất
            self.epsilon = max(0.1, self.epsilon * self.epsilon_decay)

            # Thêm thông báo tiến trình sau mỗi 50 tập để theo dõi quá trình huấn luyện
            if episode % 50 == 0:
                print(f"Hoàn thành tập {episode}/{episodes}")


    def get_solution_path(self, state):
        puzzle = Puzzle(state)
        path = []
        while not puzzle.is_goal():
            state = puzzle.to_tuple()
            actions = puzzle.get_actions()
            best_action = self.choose_action(state, actions)
            path.append(puzzle.state)
            puzzle = puzzle.move(best_action)
        path.append(puzzle.state)
        return path

if __name__ == "__main__":
    initial_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
    q_solver = QLearningSolver()
    q_solver.train(initial_state, episodes=500)
    solution_path = q_solver.get_solution_path(initial_state)

    for step, state in enumerate(solution_path):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print("---")