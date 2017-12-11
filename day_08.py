"""Solutions to day 8 parts 1 and 2."""
import re
from operator import lt, gt, ge, le, eq, ne, add, sub

PART1_TEST_INSTRUCTIONS = \
"""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

COMPARATORS = {
    "<": lt,
    ">": gt,
    ">=": ge,
    "<=": le,
    "==": eq,
    "!=": ne
}

OPERATIONS = {
    "inc": add,
    "dec": sub
}

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def parse_line(line):
    """Parse single line of instructions as."""
    register, \
        operator, \
        operator_value, \
        comparator_register, \
        comparator, \
        comparator_value = \
        re.match(r'(\w+) (\w+) (-?\d+) if (\w+) (<|>|>=|==|<=|!=) (-?\d+)', line).groups()

    return register, \
        operator, \
        int(operator_value), \
        comparator_register, \
        comparator, \
        int(comparator_value)

assert parse_line('b inc 5 if a > 1') == ('b', 'inc', 5, 'a', '>', 1)

def get_register(registers, register):
    """Return value in specified register or 0."""
    return registers.get(register) or 0

def evaluate_line(registers, register, operator, operator_value, comparator_register, comparator, comparator_value):
    """Evaluate a parsed line of instructions."""
    comparator = COMPARATORS[comparator]
    if comparator(get_register(registers, comparator_register), comparator_value):
        registers[register] = OPERATIONS[operator](
            get_register(registers, register), operator_value)

    return registers

assert evaluate_line({}, *parse_line('b inc 5 if a == 0')) == {'b': 5}

def run_program(program):
    """Run a block of instructions."""
    registers = {}
    for parsed_line in [parse_line(line) for line in program.splitlines()]:
        evaluate_line(registers, *parsed_line)

    return registers

# Part 1 test cases
assert max(run_program(PART1_TEST_INSTRUCTIONS).values()) == 1

# Part 1 solution
print("Solution to part 1: {}".format(max(run_program(load(8).read()).values())))

def run_program_part_2(program):
    """Return high water mark."""
    registers = {}
    high_water_mark = 0
    for parsed_line in [parse_line(line) for line in program.splitlines()]:
        evaluate_line(registers, *parsed_line)
        current_max = max(registers.values())
        high_water_mark = current_max if current_max > high_water_mark else high_water_mark

    return high_water_mark

# Part 2 solution
print("Solution to part 2: {}".format(run_program_part_2(load(8).read())))

