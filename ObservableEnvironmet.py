import copy
from collections import deque
import heapq, random, math, copy

# ======= AGENT ======= #

class Puzzle:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state  
        self.parent = parent
        self.move = move
        self.depth = depth
        self.blank_pos = self.find_blank()
        self.heuristic = 0

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
    
    def __lt__(self, other):
        return self.depth < other.depth


# ======= SUPPORTED FUNCTION ======= #

def manhattan_distance(state):
    goal = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
    }
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = goal[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

# ======= ALGORITHMS ======= #

# Nhóm Thuật toán tìm kiếm KHÔNG CÓ thông tin

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
        for neighbor in reversed(current.get_neighbors()):
            if neighbor.to_tuple() not in visited:
                stack.append(neighbor)
    return []

def dls(start_state, limit = 50):
    start = Puzzle(start_state)
    visited = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current.is_goal():
            return current.get_path()
        visited.add(current.to_tuple())
        if current.depth < limit:
            for neighbor in reversed(current.get_neighbors()):
                if neighbor.to_tuple() not in visited:
                    stack.append(neighbor)
    return []

def ucs(start_state):
    start = Puzzle(start_state)
    visited = set()
    queue = [(0, start)]  # (cost, node)
    while queue:
        cost, current = heapq.heappop(queue)
        if current.is_goal():
            return current.get_path()
        visited.add(current.to_tuple())
        for neighbor in current.get_neighbors():
            if neighbor.to_tuple() not in visited:
                heapq.heappush(queue, (neighbor.depth, neighbor))
    return []

def ids(start_state, max_depth=50):
    def dls(node, depth, visited):
        if node.is_goal():
            return node.get_path()
        if depth == 0:
            return None
        visited.add(node.to_tuple())
        for neighbor in node.get_neighbors():
            if neighbor.to_tuple() not in visited:
                result = dls(neighbor, depth - 1, visited)
                if result:
                    return result
        return None
    
    for depth in range(max_depth):
        start = Puzzle(start_state)
        visited = set()
        result = dls(start, depth, visited)
        if result:
            return result
    return []

# Nhóm Thuật toán tìm kiếm có thông tin

def greedy(start_state):
    start = Puzzle(start_state)
    visited = set()
    queue = [(manhattan_distance(start.state), start)]
    while queue:
        queue.sort(key=lambda x: x[0])
        _, current = queue.pop(0)
        if current.is_goal():
            return current.get_path()
        visited.add(current.to_tuple())
        for neighbor in current.get_neighbors():
            if neighbor.to_tuple() not in visited:
                queue.append((manhattan_distance(neighbor.state), neighbor))
    return []

def astar(start_state):
    start = Puzzle(start_state)
    visited = set()
    queue = [(manhattan_distance(start.state), 0, start)]
    while queue:
        queue.sort(key=lambda x: x[0])
        _, g, current = queue.pop(0)
        if current.is_goal():
            return current.get_path()
        visited.add(current.to_tuple())
        for neighbor in current.get_neighbors():
            if neighbor.to_tuple() not in visited:
                cost = g + 1
                h = manhattan_distance(neighbor.state)
                queue.append((cost + h, cost, neighbor))
    return []

def ida_star(start_state):
    def dfs_f(node, g, threshold, path, visited):
        f = g + manhattan_distance(node.state)
        if f > threshold:
            return f, None
        if node.is_goal():
            return f, path + [node.state]
        minimum = float('inf')
        for neighbor in node.get_neighbors():
            state_tuple = neighbor.to_tuple()
            if state_tuple not in visited:
                visited.add(state_tuple)
                t, result = dfs_f(neighbor, g + 1, threshold, path + [node.state], visited)
                if result:
                    return t, result
                minimum = min(minimum, t)
                visited.remove(state_tuple)
        return minimum, None

    start = Puzzle(start_state)
    threshold = manhattan_distance(start.state)
    path = []
    while True:
        visited = {start.to_tuple()}
        t, result = dfs_f(start, 0, threshold, path, visited)
        if result:
            return result
        if t == float('inf'):
            return []
        threshold = t

def simple_hill_climbing(start_state):
    current = Puzzle(start_state)
    
    while not current.is_goal():
        neighbors = current.get_neighbors()

        # Kiểm tra từng neighbor và dừng ngay khi tìm thấy neighbor tốt hơn
        for neighbor in neighbors:
            if manhattan_distance(neighbor.state) < manhattan_distance(current.state):
                current = neighbor
                break
        else:
            # Nếu không có neighbor nào tốt hơn, thoát vòng lặp
            break

    return current.get_path() if current.is_goal() else []



def steepest_ascent_hill_climbing(start_state):
    current = Puzzle(start_state)
    while True:
        neighbors = current.get_neighbors()
        best_neighbor = None
        best_h = manhattan_distance(current.state)
        for neighbor in neighbors:
            h = manhattan_distance(neighbor.state)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
        if best_neighbor is None:
            break
        current = best_neighbor
        if current.is_goal():
            return current.get_path()
    return current.get_path() if current.is_goal() else []

def stochastic_hill_climbing(start_state):
    current = Puzzle(start_state)
    while True:
        neighbors = current.get_neighbors()
        better_neighbors = [n for n in neighbors if manhattan_distance(n.state) < manhattan_distance(current.state)]
        if not better_neighbors:
            break
        current = random.choice(better_neighbors)
        if current.is_goal():
            return current.get_path()
    return current.get_path() if current.is_goal() else []

def simulated_annealing(start_state, initial_temp=1000, cooling_rate=0.95):
    current = Puzzle(start_state)
    T = initial_temp
    while T > 1:
        if current.is_goal():
            return current.get_path()
        neighbors = current.get_neighbors()
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        delta_e = manhattan_distance(current.state) - manhattan_distance(next_node.state)
        if delta_e > 0 or math.exp(delta_e / T) > random.random():
            current = next_node
        T *= cooling_rate
    return current.get_path() if current.is_goal() else []

def beam_search(start_state, width=4):
    start = Puzzle(start_state)
    visited = set()
    frontier = [start]
    visited.add(start.to_tuple())
    
    while frontier:
        new_frontier = []
        
        for node in frontier:
            if node.is_goal():
                return node.get_path()
            
            # Duyệt các trạng thái hàng xóm
            for neighbor in node.get_neighbors():
                state_tuple = neighbor.to_tuple()
                
                # Chỉ thêm vào nếu chưa duyệt qua
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    new_frontier.append(neighbor)
        
        # Sắp xếp theo hàm heuristic (Manhattan Distance)
        new_frontier.sort(key=lambda n: manhattan_distance(n.state))
        
        # Chỉ giữ lại số lượng trạng thái theo `width`
        frontier = new_frontier[:width]
    
    return []


# Genetic Alg
def flatten(state):
    return [num for row in state for num in row]

def unflatten(flat):
    return [flat[i*3:(i+1)*3] for i in range(3)]

def is_solvable(state):
    flat = flatten(state)
    inv = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] and flat[j] and flat[i] > flat[j]:
                inv += 1
    return inv % 2 == 0

def mutate(state):
    flat = flatten(state)
    i, j = random.sample(range(9), 2)
    flat[i], flat[j] = flat[j], flat[i]
    return unflatten(flat)

def crossover(parent1, parent2):
    flat1 = flatten(parent1)
    flat2 = flatten(parent2)
    idx = random.randint(1, 7)
    child_flat = flat1[:idx] + [x for x in flat2 if x not in flat1[:idx]]
    return unflatten(child_flat)

def fitness(state):
    return -manhattan_distance(state)

def shuffle_state(state, steps=30):
    state = copy.deepcopy(state)
    for _ in range(steps):
        bi, bj = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                moves.append((ni, nj))
        if moves:
            mi, mj = random.choice(moves)
            state[bi][bj], state[mi][mj] = state[mi][mj], state[bi][bj]
    return state


def genetic_algorithm(start_state, population_size=20, generations=100):
    population = [start_state]
    while len(population) < population_size:
        shuffled = shuffled = shuffle_state(start_state, steps=20)
        if is_solvable(shuffled):
            population.append(shuffled)

    for _ in range(generations):
        scored = sorted([(fitness(ind), ind) for ind in population], reverse=True)
        if scored[0][0] == 0:
            return bfs(scored[0][1])
        new_population = [scored[0][1]]
        while len(new_population) < population_size:
            parents = random.choices(scored[:10], k=2)
            child = crossover(parents[0][1], parents[1][1])
            if random.random() < 0.3:
                child = mutate(child)
            if is_solvable(child):
                new_population.append(child)
        population = new_population
    best = max(population, key=lambda s: fitness(s))
    return bfs(best)  # fallback to BFS from best found
