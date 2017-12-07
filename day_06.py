"""Solution to day 6 parts and and 2."""
import re

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def parse(memory_representation):
    """Parse memory state to array."""
    return [int(block) for block in re.findall(r'\d+', memory_representation)]

def balance_memory(configuration):
    """Balance blocks across entire memory."""
    blocks_to_reallocate = max(configuration)
    block_index = configuration.index(blocks_to_reallocate)
    configuration[block_index] = 0
    while blocks_to_reallocate:
        block_index = (block_index + 1) % len(configuration)
        configuration[block_index] += 1
        blocks_to_reallocate -= 1

    return configuration

def reallocate_memory(configuration):
    """Balance memory until previous memory configuration is repeated."""
    history = set()
    memory_state = tuple(configuration)
    reallocation_attempts = 0

    while memory_state not in history:
        history.add(memory_state)
        configuration = balance_memory(configuration)
        memory_state = tuple(configuration)
        reallocation_attempts += 1

    return reallocation_attempts

# Part 1 test cases
assert reallocate_memory([0, 2, 7, 0]) == 5

# Part 1 solution
print("Solution to part 1: {}".format(reallocate_memory(parse(load(6).read()))))

def reallocate_memory_with_distance(configuration):
    """Balance memory until previous memory configuration is repeated.
    Calculate the distance between repeated states"""
    history = {}
    memory_state = tuple(configuration)
    reallocation_attempts = 0

    while memory_state not in history:
        history[memory_state] = reallocation_attempts
        configuration = balance_memory(configuration)
        memory_state = tuple(configuration)
        reallocation_attempts += 1

    return reallocation_attempts - history[memory_state]

# Part 2 test cases
assert reallocate_memory_with_distance([0, 2, 7, 0]) == 4

# Part 2 solution
print("Solution to part 2: {}".format(reallocate_memory_with_distance(parse(load(6).read()))))
