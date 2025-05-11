import copy

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
        return None

    def get_neighbors(self):
        neighbors = []
        bi, bj = self.blank_pos
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = copy.deepcopy(self.state)
                new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
                neighbors.append(Puzzle(new_state, parent=self, move=(di, dj), depth=self.depth + 1))
        return neighbors

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]


def backtracking_solve(initial_state, max_depth=100):
    initial_puzzle = Puzzle(initial_state)
    visited = set()
    return backtrack(initial_puzzle, visited, max_depth)


def backtrack(puzzle, visited, max_depth):
    if puzzle.depth > max_depth:
        return []
    state_tuple = tuple(tuple(row) for row in puzzle.state)
    if state_tuple in visited:
        return []
    visited.add(state_tuple)

    if puzzle.is_goal():
        return puzzle.get_path()

    for neighbor in puzzle.get_neighbors():
        result = backtrack(neighbor, visited, max_depth)
        if len(result)>0:
            return result

    visited.remove(state_tuple)
    return []


def backtracking_solve_with_forward_checking(initial_state, max_depth=100):
    initial_puzzle = Puzzle(initial_state)
    visited = set()
    return backtrack_with_forward_checking(initial_puzzle, visited, max_depth)


def backtrack_with_forward_checking(puzzle, visited, max_depth):
    if puzzle.depth > max_depth:
        return []
    state_tuple = tuple(tuple(row) for row in puzzle.state)
    if state_tuple in visited:
        return []
    visited.add(state_tuple)

    if puzzle.is_goal():
        return puzzle.get_path()

    for neighbor in puzzle.get_neighbors():
        # Forward checking: Only proceed if neighbor is closer to goal
        misplaced = sum(1 for i in range(3) for j in range(3) if neighbor.state[i][j] != 0 and neighbor.state[i][j] != (i * 3 + j + 1) % 9)
        current_misplaced = sum(1 for i in range(3) for j in range(3) if puzzle.state[i][j] != 0 and puzzle.state[i][j] != (i * 3 + j + 1) % 9)

        if misplaced < current_misplaced:
            result = backtrack_with_forward_checking(neighbor, visited, max_depth)
            if len(result)>0:
                return result

    visited.remove(state_tuple)
    return []


# Example usage
if __name__ == "__main__":
    initial_state = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]

    print("Backtracking without Forward Checking:")
    solution_path = backtracking_solve(initial_state, max_depth=200)
    if solution_path:
        for step in solution_path:
            for row in step:
                print(row)
            print("---")
    else:
        print("No solution found.")

    # print("\nBacktracking with Forward Checking:")
    # solution_path = backtracking_solve_with_forward_checking(initial_state, max_depth=200)
    # if solution_path:
    #     for step in solution_path:
    #         for row in step:
    #             print(row)
    #         print("---")
    # else:
    #     print("No solution found.")
