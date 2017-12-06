"""Solution to day 5 parts 1 and 2."""

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename).read()

# Part 1

def jump(offsets, cursor=0, steps=0):
    """Perform the steps defined in the offsets list.
    Exit when jumped out of bounds of list of offsets"""
    cursor, steps = 0, 0

    while cursor >= 0 and cursor < len(offsets):
        jump_size = offsets[cursor]
        offsets[cursor] = offsets[cursor] + 1
        cursor += jump_size
        steps += 1

    return steps

# Part 1 test cases
assert jump([0, 3, 0, 1, -3]) == 5

def parse_offsets(offsets):
    """Parse offsets file into list of offsets."""
    return [int(offset) for offset in offsets.splitlines()]

# Solution to part 1
print("Solution to part 1: {}".format(jump(parse_offsets(load(5)))))

# Part 2

def in_bounds(offsets, cursor):
    """Return if the current cursor location is in the bounds
    of the suppplied offsets list."""
    return cursor >= 0 and cursor < len(offsets)

def day_2_strategy(offset):
    """Return the new offset given the current value."""
    return offset - 1 if offset >= 3 else offset + 1

def jump_with_strategy(offsets, strategy):
    """Perform the steps defined in the offsets list.
    Use supplied strategy to update the jumped from location."""
    cursor, steps = 0, 0

    while in_bounds(offsets, cursor):
        offset = offsets[cursor]
        offsets[cursor] = strategy(offset)
        cursor += offset
        steps += 1

    return steps

# Part 2 test cases
assert(jump_with_strategy([0, 3, 0, 1, -3], day_2_strategy)) == 10

# Solution to part 2
print("Solution to part 2: {}".format(
    jump_with_strategy(parse_offsets(load(5)), day_2_strategy)))
