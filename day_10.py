"""Solution to day 10 parts 1 and 2."""
from functools import reduce
from operator import xor

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def tie_knot(numbers, cursor, length):
    """Split list in to 3 parts and note if a wrap-around occured."""
    size_of_list = len(numbers)
    will_wrap = (cursor + length) >= size_of_list
    head, tail = [], []

    if not will_wrap:
        head = numbers[cursor:cursor + length]
        tail = numbers[cursor + length:] + numbers[:cursor]
    else:
        wrap_end = (cursor + length) % size_of_list
        head = numbers[cursor:] + numbers[0:(cursor + length) % size_of_list]
        tail = numbers[wrap_end:wrap_end + size_of_list - length]

    return head, tail

def rotate_list(numbers, cursor):
    """Rotate list such that the current start moves to the position
    indicated by the cursor."""
    return numbers[len(numbers) - cursor:] + numbers[:len(numbers) - cursor]

def tie_knots(numbers, lengths):
    """Tie the knots specified by the lengths array."""
    cursor, skip_size = 0, 0

    for length in lengths:
        head, tail = tie_knot(numbers, cursor, length)
        numbers = rotate_list(list(reversed(head)) + tail, cursor)
        cursor = (cursor + length + skip_size) % len(numbers)
        skip_size += 1

    return numbers

def checksum(numbers):
    """Form checksum from list of numbers."""
    return numbers[0] * numbers[1]

# Part 1 test cases
assert tie_knots([0, 1, 2, 3, 4], [3, 4, 1, 5]) == [3, 4, 2, 1, 0]

# Solution to part 1
print("Solution to part 1: {}".format(
    checksum(
        tie_knots(list(range(256)), [int(number) for number in load(10).read().split(',')]))))

def convert_to_ascii(lengths):
    """Convert from numbers to associated ascii values."""
    return [ord(length) for length in lengths]

def parse_numbers(numbers):
    """Parse numbers string to list of ascii values."""
    termination = [17, 31, 73, 47, 23]
    return convert_to_ascii(
        [number for number in numbers]) + termination

def tie_knots_multiple_rounds(numbers, lengths, rounds):
    """Tie the knots specified by the lengths array."""
    cursor, skip_size = 0, 0

    for _ in range(rounds):
        for length in lengths:
            head, tail = tie_knot(numbers, cursor, length)
            numbers = rotate_list(list(reversed(head)) + tail, cursor)
            cursor = (cursor + length + skip_size) % len(numbers)
            skip_size += 1

    return numbers

def form_chunks(numbers, chunk_size):
    """Form list chunks."""
    for cursor in range(0, len(numbers), chunk_size):
        yield numbers[cursor:cursor + chunk_size]

def form_dense_hash(numbers):
    """Form dense hash of list numbers."""
    return [reduce(xor, chunk) for chunk in list(form_chunks(numbers, 16))]

def form_hex(dense_hash):
    """Hexadecimal encoding from dense hash."""
    return ''.join([format(number, '02x') for number in dense_hash])

def hex_checksum():
    """Wrapper for part 2."""
    numbers = parse_numbers(load(10).read())
    knots = tie_knots_multiple_rounds(list(range(256)), numbers, 64)
    dense_hash = form_dense_hash(knots)
    hex_encoding = form_hex(dense_hash)
    return hex_encoding

print('Solution to part 2: {}'.format(hex_checksum()))
