import copy
import random

class Puzzle:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.blank_pos = self.find_next_blank()

    def find_next_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0 and i + j != 4:
                    return (i, j)
        return None

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    def get_domain(self):
        used_values = set(sum(self.state, []))
        return [i for i in range(1, 9) if i not in used_values]

    def forward_checking(self, value):
        bi, bj = self.blank_pos

        # Kiểm tra giá trị có trong domain
        if value not in self.get_domain():
            return False

        # Kiểm tra điều kiện phải lớn hơn ô kề trước đó
        previous_values = []
        if bi > 0 and self.state[bi - 1][bj] != 0:
            previous_values.append(self.state[bi - 1][bj])  # Ô bên trên
        if bj > 0 and self.state[bi][bj - 1] != 0:
            previous_values.append(self.state[bi][bj - 1])  # Ô bên trái

        # Nếu không có ô kề trước, giá trị hợp lệ
        if not previous_values:
            return True

        # Kiểm tra điều kiện giá trị phải lớn hơn tất cả các ô kề trước
        return all(value > prev for prev in previous_values)

    def conflict_difference(self, bi, bj, value):
        pi, pj = bi, bj
        if bi > 0 and self.state[bi - 1][bj] != 0:
            pi = pi - 1  # Ô bên trên
        if bj > 0 and self.state[bi][bj - 1] != 0:
            pj = pj - 1 # Ô bên trái
        if pi + pj == 0:
            return 0
        if (self.state[pi][pj] < value):
            return value - self.state[pi][pj]
        return 9



# Backtracking Algorithm
def backtracking_fill(initial_state, max_depth=1000):
    initial_puzzle = Puzzle(initial_state)
    visited = set()
    return fill_backtrack(initial_puzzle, visited, 1, max_depth)


def fill_backtrack(puzzle, visited, num, max_depth):
    if puzzle.depth > max_depth:
        return None

    state_tuple = tuple(tuple(row) for row in puzzle.state)
    if state_tuple in visited:
        return None
    visited.add(state_tuple)

    if puzzle.is_goal():
        return puzzle.get_path()

    next_blank = puzzle.find_next_blank()
    if not next_blank:
        return None

    bi, bj = next_blank

    for value in range(1, 9):
        new_state = copy.deepcopy(puzzle.state)
        new_state[bi][bj] = value
        next_puzzle = Puzzle(new_state, parent=puzzle, depth=puzzle.depth + 1)
        result = fill_backtrack(next_puzzle, visited, num + 1, max_depth)
        if result:
            return result

    visited.remove(state_tuple)
    return None


# Backtracking with Forward Checking Algorithm
def forward_checking_fill(initial_state, max_depth=1000):
    initial_puzzle = Puzzle(initial_state)
    visited = set()
    return fill_forward_check(initial_puzzle, visited, 1, max_depth)


def fill_forward_check(puzzle, visited, num, max_depth):
    if puzzle.depth > max_depth:
        return None

    state_tuple = tuple(tuple(row) for row in puzzle.state)
    if state_tuple in visited:
        return None
    visited.add(state_tuple)

    if puzzle.is_goal():
        return puzzle.get_path()

    next_blank = puzzle.find_next_blank()
    if not next_blank:
        return None

    bi, bj = next_blank

    for value in range(1, 9):
        # Forward Checking
        if puzzle.forward_checking(value):
            new_state = copy.deepcopy(puzzle.state)
            new_state[bi][bj] = value
            next_puzzle = Puzzle(new_state, parent=puzzle, depth=puzzle.depth + 1)
            result = fill_forward_check(next_puzzle, visited, num + 1, max_depth)
            if result:
                return result

    visited.remove(state_tuple)
    return None


# Min-Conflict Local Search Algorithm
def min_conflict_fill(initial_state, max_steps=1000):
    puzzle = Puzzle(initial_state)

    for _ in range(max_steps):
        if puzzle.is_goal():
            return puzzle.get_path()

        blank_positions = [(i, j) for i in range(3) for j in range(3) if puzzle.state[i][j] == 0]
        if not blank_positions:
            break

        bi, bj = random.choice(blank_positions)
        #bi, bj = puzzle.find_next_blank()
        min_conflicts = float('inf')
        best_value = None

        for value in puzzle.get_domain():
            conflict_count = puzzle.conflict_difference(bi, bj, value)
            if conflict_count < min_conflicts:
                min_conflicts = conflict_count
                best_value = value

        puzzle.state[bi][bj] = best_value

    return []


# Example usage
if __name__ == "__main__":
    initial_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # print("Backtracking Solution:")
    # solution_path = backtracking_fill(initial_state, max_depth=20)
    # if solution_path:
    #     for step in solution_path:
    #         for row in step:
    #             print(row)
    #         print("---")
    # else:
    #     print("No solution found using Backtracking.")

    # print("\nForward Checking Solution:")
    # solution_path = forward_checking_fill(initial_state, max_depth=20)
    # if solution_path:
    #     for step in solution_path:
    #         for row in step:
    #             print(row)
    #         print("---")
    # else:
    #     print("No solution found using Forward Checking.")

    print("\nMin-Conflict Solution:")
    solution_path = min_conflict_fill(initial_state, max_steps=1000)
    if solution_path:
        for step in solution_path:
            for row in step:
                print(row)
            print("---")
    else:
        print("No solution found using Min-Conflict.")
