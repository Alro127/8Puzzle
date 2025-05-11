import copy
from graphviz import Digraph

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


class BeliefState:
    def __init__(self, states):
        self.states = states

    def update(self):
        new_belief = set()
        for state in self.states:
            for neighbor in state.get_neighbors():
                if neighbor not in new_belief:
                    new_belief.add(neighbor)
        return BeliefState(new_belief)

    def find_goal_node(self):
        for state in self.states:
            if state.is_goal():
                return state
        return None


class GraphVisualizer:
    def __init__(self):
        self.graph = Digraph(node_attr={'shape': 'box', 'style': 'rounded'});
        self.graph.attr(rankdir='TB')
        self.visited_nodes = {}

    def add_node(self, node, highlight=False):
        if node.node_id not in self.visited_nodes:
            label = '\n'.join([' '.join(map(str, row)) for row in node.state])
            color = 'red' if highlight else 'black'
            self.graph.node(node.node_id, label=label, color=color)
            self.visited_nodes[node.node_id] = node.node_id

    def add_edge(self, parent, child, highlight=False):
        color = 'red' if highlight else 'black'
        self.graph.edge(parent.node_id, child.node_id, color=color)

    def highlight_path(self, goal_node):
        path = goal_node.get_path()
        for i in range(len(path) - 1):
            self.add_node(path[i], highlight=True)
            self.add_edge(path[i], path[i + 1], highlight=True)
        self.add_node(path[-1], highlight=True)

    def save_graph(self, filename):
        self.graph.render(filename, format='png', cleanup=True)


def belief_state_search(initial_belief, visualizer):
    current_belief = initial_belief
    
    while True:
        for node in current_belief.states:
            visualizer.add_node(node)
            if node.parent:
                visualizer.add_edge(node.parent, node)
        goal_node = current_belief.find_goal_node()
        if goal_node:
            return goal_node

        current_belief = current_belief.update()
        if not current_belief.states:
            print("No solution found")
            return None


# Example usage with multiple initial states
state1 = Puzzle([[1, 2, 3], [4, 5, 6], [0, 7, 8]])
state2 = Puzzle([[1, 2, 3], [4, 5, 0], [7, 6, 8]])
state3 = Puzzle([[1, 2, 3], [4, 0, 6], [7, 5, 8]])

initial_belief = BeliefState({state1, state2, state3})
visualizer = GraphVisualizer()
goal_node = belief_state_search(initial_belief, visualizer)

if goal_node:
    print("Goal Node Found. Path to goal:")
    for step in goal_node.get_path():
        for row in step.state:
            print(row)
        print("-----")
    visualizer.highlight_path(goal_node)
    visualizer.save_graph("belief_state_graph")
else:
    print("No solution found")