"""Solution to day 3 part 1 and 2"""
import math

# Part I

def dimension_of_bounding_square(number):
    """Find the smallest binding square, e.g.
    1x1, 3x3, 5x5
    Approach is to assume that the number is the largest
    that the bounding square can contain.
    Hence taking the square root will find the length of the
    side of the bounding square.
    The actual bounding squares all have integer length that is odd
    ( due to the wrapping action of forming a spiral)
    Hence find the actual length by rounding the square root to the next
    integer odd number."""
    approximate_dimension = math.ceil((math.sqrt(number)))
    return approximate_dimension + (1 - (approximate_dimension % 2))

assert dimension_of_bounding_square(1) == 1
assert dimension_of_bounding_square(2) == 3
assert dimension_of_bounding_square(9) == 3
assert dimension_of_bounding_square(10) == 5
assert dimension_of_bounding_square(24) == 5

def find_middle_of_edges(edge_length):
    """Returns array of all numbers at the middle of an edge"""
    if edge_length == 1:
        return [1, 1, 1, 1]

    bottom_right = int(math.pow(edge_length, 2))
    gap_to_middle = int(edge_length / 2)
    middle_of_edges = [bottom_right - gap_to_middle]
    for idx in range(3):
        middle_of_edges.append(middle_of_edges[idx] - edge_length + 1)

    return sorted(middle_of_edges)

assert find_middle_of_edges(1) == [1, 1, 1, 1]
assert find_middle_of_edges(3) == [2, 4, 6, 8]
assert find_middle_of_edges(5) == [11, 15, 19, 23]

def distance_to_closest_middle_of_edge(middle_of_edges, number):
    """Returns the difference between the supplied number
    and the closest middle edge"""
    return min(map(lambda middle: abs(middle - number), middle_of_edges))

assert distance_to_closest_middle_of_edge([1, 1, 1, 1], 1) == 0
assert distance_to_closest_middle_of_edge([2, 4, 6, 8], 2) == 0
assert distance_to_closest_middle_of_edge([11, 15, 19, 23], 13) == 2

def find_distance(number):
    """Finds the distance between a number and 1"""
    dimension = dimension_of_bounding_square(number)
    middles = find_middle_of_edges(dimension)
    distance = distance_to_closest_middle_of_edge(middles, number)
    return distance + int(dimension / 2)

# Part 1 test cases
assert find_distance(1) == 0
assert find_distance(12) == 3
assert find_distance(23) == 2
assert find_distance(1024) == 31

# Solution to part 1
print("Solution to part 1: {}".format(find_distance(347991)))

#
# Initial solution to part 1 is too specialized and does not extend to part 2
#
Point = complex
N, S, E, W = 1j, -1j, 1, -1 # Unit vectors for headings

def manhatten_distance(point):
    """Manhatten distance between point and the origin."""
    return int(abs(point.real) + abs(point.imag))

def find_bottom_right(edge_length):
    """Calculate bottom right of current square."""
    middle_point = int(edge_length / 2)
    return  complex(middle_point, -middle_point)

def at_end_of_edge(point, edge_length):
    """Calculate if we are at the end of the edge of the current square."""
    middle_point = int(edge_length / 2)
    return abs(point.real) == middle_point and abs(point.imag) == middle_point

def off_square(point, edge_length):
    """Calculate if we have jumped off the current square"""
    middle_point = int(edge_length / 2)
    return abs(point.real) > middle_point or abs(point.imag) > middle_point

def move(termination_number):
    """Keep spiralling until we reach the number
    that matches the termination_condition."""
    number = 1 # Begin with a 1 at the origin
    edge_length = 1 # Start on square with edge 1
    bottom_right = find_bottom_right(edge_length)
    location, heading = 0, E # Begin at the origin facing East

    # Keep spiralling until we reach the desired numer
    while number < termination_number:
        # If we have jumped off the current square, rotate left
        if off_square(location, edge_length):
            heading *= N
            # Recalcuate the lenght of the edge of the current square
            edge_length += 2
            # Find the bottom right of the current square
            bottom_right = find_bottom_right(edge_length)

        # If we are at the end of the edge but NOT at the bottom right
        # then also turn left
        if at_end_of_edge(location, edge_length) and location != bottom_right:
            heading *= N

        # Move forward one
        location += heading

        # Populate the current space
        number += 1
    return location

# Part 1 test cases
assert manhatten_distance(move(1)) == 0
assert manhatten_distance(move(12)) == 3
assert manhatten_distance(move(23)) == 2
assert manhatten_distance(move(1024)) == 31

# Solution to part 1
print("Solution to part 1: {}".format(manhatten_distance(move(347991))))

# Part II

def find_neighbors(location):
    """Return list of all adjacent locations."""
    neighbors = []
    for x_translation in range(-1, 2):
        for y_translation in range(-1, 2):
            if x_translation == 0 and y_translation == 0:
                continue
            translation = complex(x_translation, y_translation)
            neighbors.append(location + translation)
    return neighbors

assert find_neighbors(complex(0)) == [
    complex(-1, -1),
    complex(-1),
    complex(-1, 1),
    complex(0, -1),
    complex(0, 1),
    complex(1, -1),
    complex(1),
    complex(1, 1)
]

def part_two_strategy(history, location):
    """Calculate the value of the current location
    given the history of values for previous locations"""
    values = [history.get(neighbor, 0) for neighbor in find_neighbors(location)]
    return sum(values)

assert part_two_strategy({complex(0): 1}, complex(1, 0)) == 1
assert part_two_strategy(
    {
        complex(0): 1,
        complex(1): 1,
        complex(1, 1): 2
    },
    complex(0, 1)) == 4

def solve_part_two(termination_threshold, strategy):
    """Keep spiralling around in concentric squares until the value
    of the current location is greater than the specifed termination
    threshold."""
    location, heading = 0, E # Start at the origin facing east
    edge_length = 1 # Start on square with edge length 1
    bottom_right = 0
    history = {location: 1}

    while history[location] <= termination_threshold:

        print("baz")

        # deal with heading:
        # if off the current square jump to next and turn left
        if off_square(location, edge_length):
            heading *= N
            edge_length += 2
            bottom_right = find_bottom_right(edge_length)
        # if we are at any vertex except the bottom right
        # turn left to stay on the perimeter of the square
        if at_end_of_edge(location, edge_length) and location != bottom_right:
            heading *= N

        # Move forward 1 using the current heading
        location += heading
        print(location)

        # Calculate value of current location on the path
        history[location] = strategy(history, location)

    return history[location]

assert solve_part_two(1, part_two_strategy) == 2
assert solve_part_two(133, part_two_strategy) == 142
print("Solution to part 2: {}".format(solve_part_two(347991, part_two_strategy)))
