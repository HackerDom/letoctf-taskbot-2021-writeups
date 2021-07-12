from collections import defaultdict
from os import urandom
from random import shuffle, choice
from string import printable

ALL_STATES = list(range(9))

NODES = [
    ('L', 'W', 0, 1),
    ('e', 'r', 1, 1),
    ('t', '0', 1, 2),
    ('o', 'n', 2, 2),
    ('C', 'g', 2, 2),
    ('T', 'W', 2, 2),
    ('F', '4', 2, 8),
    ('{', 'y', 8, 8),

    ('F', 'f', 3, 1),
    ('A', 'l', 1, 4),
    ('k', '4', 4, 4),
    ('3', 'g', 4, 4),
    ('_', '}', 4, 8),

    ('L', '0', 0, 0),
    ('e',   0, 0, 0),
    ('t', 'n', 0, 0),
    ('o', 'l', 0, 0),
    ('C', 'y', 0, 0),
    ('T',   0, 0, 3),
    ('F', '_', 3, 3),
    ('{',   0, 3, 3),
    ('N', '4', 3, 5),
    ('F', '_', 5, 5),
    ('A',   0, 5, 5),
    ('_',   0, 5, 5),
    ('i', 'r', 5, 6),
    ('5',   0, 6, 5),
    ('g', '3', 5, 6),
    ('0',   0, 6, 5),
    ('0', 'g', 5, 6),
    ('d', 'E', 6, 6),
    ('_',   0, 6, 7),
    ('n', 'x', 7, 7),
    ('0', 'p', 7, 7),
    ('t', '5', 7, 7),
    ('_', '}', 7, 8)
]


def _converter(x):
    return ord(x) if type(x) is str else x


def _get_state(i):
    return choice(ALL_STATES) if i != 8 else 8

class Node:
    def __init__(self, _from, _to, _next_state):
        self._from = _converter(_from)
        self._to = _converter(_to)
        self._next_state = _next_state
    
    def __str__(self):
        return f"(Node){{.from = {self._from}, .to = {self._to}, .next_state = {self._next_state}}};"


def generate_flag(states):
    for node in NODES:
        c_from, c_to, s_from, s_to = node
        states[s_from].append(Node(c_from, c_to, s_to))

    return states


def add_fake_states(states):
    alpha = set(printable.encode())
    for i in range(len(states)):
        remaining_states = 256 - len(states[i])
        batch_size = remaining_states // 3

        c_froms = {x._from for x in states[i]}
        good_random_bytes = set(range(0x100)) - c_froms
        good_printable = good_random_bytes & alpha
        good_unprintable = good_random_bytes - good_printable

        good_printable, good_unprintable = map(list, (good_printable, good_unprintable))
        states[i].extend([
            Node(choice(good_printable), choice(good_unprintable), _get_state(i))
            for _ in range(batch_size)
        ])
        states[i].extend([
            Node(choice(good_unprintable), choice(good_printable), _get_state(i))
            for _ in range(batch_size)
        ])
        states[i].extend([
            Node(choice(good_unprintable), choice(good_unprintable), _get_state(i))
            for _ in range(remaining_states - 2*batch_size)
        ])

    return states


def add_loops(states):
    for i in range(len(states)):
        states[i].append(Node(0, 0, i))
    return states


def shuffle_states(states):
    for i in range(len(states)):
        shuffle(states[i])
    return states


def states_to_c(states):
    for i in range(len(states)):
        res = '\n'.join(
            f'\tstates[{i}][{j}] = {str(state)}'
            for j, state in enumerate(states[i])
        )
        print(res)


if __name__ == '__main__':
    states = defaultdict(list)
    states = generate_flag(states)
    states = add_loops(states)
    states = add_fake_states(states)
    states = shuffle_states(states)

    states_to_c(states)