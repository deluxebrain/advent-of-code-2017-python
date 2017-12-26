"""Solution to day 13 parts 1 and 2"""
import re

FIREWALL = """0: 3
1: 2
4: 4
6: 4"""


def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)


def parse_firewall_instruction(instruction):
    """Parse single firewall instruction."""
    layer, depth = re.match(r'(\d+):\s(\d+)', instruction).groups()
    return int(layer), int(depth)


assert parse_firewall_instruction("1: 2") == (1, 2)


def parse_firewall(definition):
    """Parse firewall definition to data structure."""
    return {layer: depth for layer, depth in map(
        parse_firewall_instruction, definition.splitlines())}


assert parse_firewall(FIREWALL) == {
    0: 3,
    1: 2,
    4: 4,
    6: 4
}


def severity_cost_function(layer, depth):
    return layer * depth


def calculate_trip_severity(firewall, cost_function, offset=0):
    """ Example for depth 3
    0   0
    1   1
    2   2
    3   1
    4   0
    5   1
    6   2
    7   1
    8   0
    """
    severity = 0
    for layer, depth in firewall.items():
        if (layer + offset) % (2 * (depth - 1)) == 0:
            severity += cost_function(layer, depth)

    return severity


assert calculate_trip_severity(parse_firewall(FIREWALL), severity_cost_function) == 24


print("Solution to part 1: {}".format(
    calculate_trip_severity(
        parse_firewall(load(13).read()),
        severity_cost_function)))


def collision_cost_function(layer, depth):
    return 1


def wait_for_safe_firewall_traversal(firewall, cost_function):
    wait = 0
    while calculate_trip_severity(firewall, cost_function, wait):
        wait += 1
    return wait


assert (wait_for_safe_firewall_traversal(parse_firewall(FIREWALL), collision_cost_function)) == 10


print("Solution to part 2: {}".format(
    wait_for_safe_firewall_traversal(
        parse_firewall(load(13).read()),
        collision_cost_function)))
