import copy, random
from graphviz import Digraph
import tracemalloc, timeit

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

    def get_actions(self):
        actions = []
        bi, bj = self.blank_pos
        for di, dj in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                actions.append((di, dj))
        return actions

    def get_possible_puzzle(self, action):
        bi, bj = self.blank_pos
        ni, nj = bi + action[0], bj + action[1]
        new_state = copy.deepcopy(self.state)
        new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
        puzzle1 = Puzzle(new_state, parent=self, move=(ni, nj), depth=self.depth + 1)

        positions = [(i, j) for i in range(3) for j in range(3)]
        (i1, j1), (i2, j2) = random.sample(positions, 2)
        new_state = copy.deepcopy(puzzle1.state)
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        puzzle2 = Puzzle(new_state, parent=self, move=(ni, nj), depth=self.depth + 1)

        return [puzzle1, puzzle2]

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def to_tuple(self):
        return tuple(tuple(row) for row in self.state)

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

class GraphVisualizer:
    def __init__(self):
        self.graph = Digraph(node_attr={'shape': 'box', 'style': 'rounded'})
        self.graph.attr(rankdir='TB')
        self.visited_nodes = {}
        self.goal_paths = []
        self.goal_nodes = []  # Lưu trữ các node đích

    def add_node(self, node, highlight=False):
        color = 'red' if highlight else 'black'
        label = '\n'.join([' '.join(map(str, row)) for row in node.state])
        self.graph.node(node.node_id, label=label, color=color)
        self.visited_nodes[node.node_id] = node.node_id

    def add_action_node(self, parent, action):
        action_id = f"{parent.node_id}_action_{action}"
        label = f" {action} "
        self.graph.node(action_id, label=label, shape="rectangle", style="filled", fillcolor="lightblue")
        self.graph.edge(parent.node_id, action_id)
        return action_id

    def add_edge(self, parent, child, action_node_id):
        self.graph.edge(action_node_id, child.node_id)

    def highlight_path(self, path):
        for i in range(len(path) - 1):
            self.add_node(path[i], highlight=True)
        self.add_node(path[-1], highlight=True)

    def render(self, filename="and_or_search_tree"):  
        self.graph.render(filename, format="png", cleanup=True)

def and_or_search(node, visualizer):
    return or_search(node, [], visualizer)


def and_search(nodes, path, visualizer):
    plan_list = []
    for new_node in nodes:
        plan = or_search(new_node, path, visualizer)
        if plan is None:
            return None
        plan_list.append(plan)
    return plan_list


def or_search(node, path, visualizer):
    visualizer.add_node(node)

    if node.is_goal():
        goal_path = []
        current = node
        while current:
            goal_path.append(current)
            current = current.parent
        goal_path = goal_path[::-1]
        visualizer.goal_paths.append(goal_path)
        visualizer.goal_nodes.append(node)  # Lưu node đích
        return []

    if node.depth > 3 or node.to_tuple() in [p.to_tuple() for p in path]:
        return None

    for action in node.get_actions():
        action_node_id = visualizer.add_action_node(node, action)
        children = node.get_possible_puzzle(action)
        for child in children:
            visualizer.add_node(child)
            visualizer.add_edge(node, child, action_node_id)

        plan = and_search(children, path + [node], visualizer)
        if plan is not None:
            return [action] + plan
    return None



if __name__ == "__main__":
    initial_state = [[1, 2, 0], [4, 5, 3], [7, 8, 6]]
    visualizer = GraphVisualizer()
    root = Puzzle(initial_state)

    tracemalloc.start()
    start_time = timeit.default_timer()

    plan = and_or_search(root, visualizer)

    end_time = timeit.default_timer()
    memory_used, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Thời gian thực thi thuật toán: {(end_time - start_time):.5f} giây")
    print(f"Bộ nhớ sử dụng: {memory_used / (1024 ** 2):.5f} MB")
    print(f"Bộ nhớ tối đa: {peak_memory / (1024 ** 2):.5f} MB")
    print("Số bước thực hiện:", len(visualizer.goal_nodes[0].get_path()))


    # Tô màu tất cả các đường dẫn đến node đích
    for path in visualizer.goal_paths:
        visualizer.highlight_path(path)

    visualizer.render()

    # In ra đường dẫn tới từng node đích
    for goal_node in visualizer.goal_nodes:
        print("Đường dẫn tới node đích:", [n for n in goal_node.get_path()])

    if plan:
        print("Kế hoạch:", plan)
