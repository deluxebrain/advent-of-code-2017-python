"""Solution to day 14 parts 1 and 2."""
from day_10 import solve as hash2

TEST_STRING = 'flqrgnkx'
PUZZLE_INPUT = 'oundnydw'

assert hash2(TEST_STRING) == '7ef846a84695f115cbd8840c616f3df7'


def form_grid(seed_string):
    grid = []
    for line in range(128):
        value = "{0}-{1}".format(seed_string, line)
        hashed_string = hash2(value)
        bit_representation = '{:0128b}'.format(int(hashed_string, 16))
        grid.append(list(map(int, bit_representation)))
    return grid


def calculate_used_squares(grid):
    used_squares = 0
    for row in grid:
        used_squares += sum(map(int, row))
    return used_squares


def find_connected_blocks(grid, row, column, seen):
    if (row, column) in seen:
        return
    if not grid[row][column]:
        return
    seen.add((row, column))

    if row > 0:
        find_connected_blocks(grid, row - 1, column, seen)
    if row < 127:
        find_connected_blocks(grid, row + 1, column, seen)
    if column > 0:
        find_connected_blocks(grid, row, column - 1, seen)
    if column < 127:
        find_connected_blocks(grid, row, column + 1, seen)


def scan_grid_for_regions(grid):
    seen = set()
    regions = 0
    for row in range(128):
        for column in range(128):
            if (row, column) in seen:
                continue
            if not grid[row][column]:
                continue
            regions += 1
            find_connected_blocks(grid, row, column, seen)

    return regions


def main():
    assert calculate_used_squares(form_grid(TEST_STRING)) == 8108

    grid = form_grid(PUZZLE_INPUT)
    print(grid)
    print('Solution to part 1: {}'.format(calculate_used_squares(grid)))

    print('Solution to part 2: {}'.format(scan_grid_for_regions(grid)))


if __name__ == "__main__":
    main()


