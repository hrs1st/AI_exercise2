import math
import numpy as np


def pick_row(sudoku, i):
    return sudoku[i]


def pick_col(sudoku, i):
    return [x[i] for x in sudoku]


def generate_block(sudoku, i, j):
    return [sudoku[i * 3 + p][j * 3 + q] for p in range(3) for q in range(3)]


def find_holes(sudoku):
    return [
        (i, j) for i in range(
            len(sudoku)
        ) for j in range(
            len(sudoku[0])
        ) if sudoku[i][j] == 0
    ]


def fill(sudoku, solution, holes):
    for i in range(len(solution)):
        sudoku[holes[i][0]][holes[i][1]] = int(solution[i])
    return sudoku


def count_conflicts(sudoku):
    conflicts = 0

    def find_conflicts(arr):
        _, counts = np.unique(arr, return_counts=True)
        return sum([math.comb(x, 2) for x in counts if x > 1])

    for i in range(len(sudoku)):
        conflicts += find_conflicts(pick_row(sudoku, i))

    for i in range(len(sudoku[0])):
        conflicts += find_conflicts(pick_col(sudoku, i))

    for i in range(len(sudoku) // 3):
        for j in range(len(sudoku[0]) // 3):
            conflicts += find_conflicts(generate_block(sudoku, i, j))

    return conflicts


def calculate_valid_genes(sudoku):
    res = []
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                res.append(
                    list(set(range(1, 10)) - (
                        set(generate_block(sudoku, i // 3, j // 3)).union(
                            set(pick_row(sudoku, i))).union(
                            set(pick_col(sudoku, j)))
                    ))
                )

    return res


def fitness(solution, sudoku, holes):
    sudoku = fill(sudoku, solution, holes)
    return math.exp(-count_conflicts(sudoku))