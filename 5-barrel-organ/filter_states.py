import re
from collections import defaultdict
from string import printable

NODE_PATTERN = re.compile(r'states\[(\d+)\]\[\d+\] = \(Node\){\.from = (\d+), \.to = (\d+), \.next_state = (\d+)\};')
ALPHA = set(b'\0' + printable.encode())

def read_states():
    states = defaultdict(list)
    with open('states.txt', 'r') as f:
        for line in f:
            node = list(map(int, NODE_PATTERN.findall(line)[0]))
            states[node[0]].append(tuple(node[1:]))

    return states


def filter_nodes(nodes):
    return [
        node for node in nodes
        if node[0] in ALPHA and node[1] in ALPHA
    ]


def printable_node(node):
    return [
        chr(node[0]) if node[0] else 0,
        chr(node[1]) if node[1] else 0,
        node[2]
    ]


if __name__ == '__main__':
    states = read_states()
    for state, nodes in states.items():
        states[state] = filter_nodes(nodes)
    
    for state, nodes in states.items():
        print(state, list(map(printable_node, nodes)))