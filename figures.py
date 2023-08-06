from collections import deque

FIGURES = [
    # I
    [[1, 1, 1, 1]],
    [[1],
     [1],
     [1],
     [1]],

    # T
    [[1, 1, 1],
     [0, 1, 0]],
    [[0, 1],
     [1, 1],
     [0, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 0],
     [1, 1],
     [1, 0]],

    # Z
    [[0, 1],
     [1, 1],
     [1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],

    # S
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 0],
     [1, 1],
     [0, 1]],

    # L
    [[1, 1, 1],
     [0, 0, 1]],
    [[1, 1],
     [1, 0],
     [1, 0]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 1],
     [0, 1],
     [1, 1]],

    # J
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 0],
     [1, 0],
     [1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1],
     [0, 1],
     [0, 1]],

    # O
    [[1, 1],
     [1, 1]],
]

rotate_piece = {}
figure_keys = ['I', 'T', 'Z', 'S', 'L', 'J', 'O']

rotate_piece[figure_keys[0]] = deque([FIGURES[0], FIGURES[1]])
rotate_piece[figure_keys[1]] = deque([FIGURES[2], FIGURES[3], FIGURES[4], FIGURES[5]])
rotate_piece[figure_keys[2]] = deque([FIGURES[6], FIGURES[7]])
rotate_piece[figure_keys[3]] = deque([FIGURES[8], FIGURES[9]])
rotate_piece[figure_keys[4]] = deque([FIGURES[10], FIGURES[11], FIGURES[12], FIGURES[13]])
rotate_piece[figure_keys[5]] = deque([FIGURES[14], FIGURES[15], FIGURES[16], FIGURES[17]])
rotate_piece[figure_keys[6]] = deque([FIGURES[18]])


FIGURES_COLOR = [
    (0, 255, 255),  # I - Cyan
    (0, 255, 255),  # I - Cyan

    (128, 0, 128),  # T - Purple
    (128, 0, 128),  # T - Purple
    (128, 0, 128),  # T - Purple
    (128, 0, 128),  # T - Purple

    (255, 0, 0),  # Z - Red
    (255, 0, 0),  # Z - Red

    (0, 255, 0),  # S - Green
    (0, 255, 0),  # S - Green

    (255, 165, 0),  # L - Orange
    (255, 165, 0),  # L - Orange
    (255, 165, 0),  # L - Orange
    (255, 165, 0),  # L - Orange

    (0, 0, 255),  # J - Blue
    (0, 0, 255),  # J - Blue
    (0, 0, 255),  # J - Blue
    (0, 0, 255),  # J - Blue

    (255, 255, 0),  # O - Yellow
]

FIGURES_COLOR_DICT = {
    'I': (0, 255, 255),
    'T': (128, 0, 128),
    'Z': (255, 0, 0),
    'S': (0, 255, 0),
    'L': (255, 165, 0),
    'J': (0, 0, 255),
    'O': (255, 255, 0),
}
