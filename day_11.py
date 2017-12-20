"""Solution to day 11 parts 1 and 2."""

HEX_RAYS = {
    'N': [0, 1, -1],
    'S': [0, -1, 1],
    'NE': [1, 0, -1],
    'NW': [-1, 1, 0],
    'SW': [-1, 0, 1],
    'SE': [1, -1, 0]
}

ORIGIN = [0, 0, 0]

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def parse_sequence(directions):
    """Parse textual representation of sequence of directions
    into a list."""
    return [direction.upper() for direction in directions.split(',')]

assert parse_sequence('ne,ne,ne') == ['NE', 'NE', 'NE']

def move(position, direction):
    """Move one unit in specifed direction."""
    return [sum(x) for x in zip(position, HEX_RAYS[direction])]

def move_sequence(position, directions):
    """Move sequentially in given directions."""
    for direction in directions:
        position = move(position, direction)

    return position

assert move_sequence(ORIGIN, parse_sequence('ne,ne,ne')) == [3, 0, -3]

def calculate_distance(position):
    """Calculate distance from position from the origin."""
    return sum(map(abs, position)) / 2

# Part 1 test cases
assert calculate_distance(move_sequence(ORIGIN, parse_sequence('ne,ne,ne'))) == 3
assert calculate_distance(move_sequence(ORIGIN, parse_sequence('ne,ne,sw,sw'))) == 0
assert calculate_distance(move_sequence(ORIGIN, parse_sequence('ne,ne,s,s'))) == 2
assert calculate_distance(move_sequence(ORIGIN, parse_sequence('se,sw,se,sw,sw'))) == 3

print("Solution to part 1: {}".format(calculate_distance(move_sequence(ORIGIN, parse_sequence(load(11).read())))))

def calculate_furthest_distance(directions, position = ORIGIN, furthest = 0):
    """Move as per directions and return max distance."""

    for direction in directions:
        position = move(position, direction)
        if calculate_distance(position) > furthest:
            furthest = calculate_distance(position)

    return furthest

print("Solution to part 2: {}".format(calculate_furthest_distance(parse_sequence(load(11).read()))))




