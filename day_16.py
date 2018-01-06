"""Day 16 parts 1 and 2."""
import string
import re
from functools import reduce


def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)


def spin(program_list, amount):
    """Rotate program list by amount from the end of the list
    e.g. abcde amount 3 gives cdeab."""
    return program_list[-amount:] + \
           program_list[:len(program_list) - amount]


def exchange(program_list, this_position, that_position):
    """Exchange program at __this__ position with program
    at __that__ position."""
    new_list = list(program_list)
    new_list[this_position] = program_list[that_position]
    new_list[that_position] = program_list[this_position]
    return "".join(new_list)


def partner(program_list, this_program, that_program):
    """Exchange __this__ program with __that__ program."""
    return exchange(program_list,
                    program_list.index(this_program),
                    program_list.index(that_program))


ACTIONS_MAP = {
    's': lambda program_list, amount: spin(program_list, int(amount)),
    'x': lambda program_list, this_position, that_position: exchange(
        program_list, int(this_position), int(that_position)),
    'p': partner
    }


def dispatch_move(program_list, move):
    action, raw_params = re.match(r'(\w)(\w+\/*\w*)', move).groups()
    params = raw_params.split('/')
    return ACTIONS_MAP[action](program_list, *params)


def perform_sequence(program_list, sequence):
    program_list = reduce(lambda current_list, move: dispatch_move(current_list, move),
                          [move for move in sequence],
                          program_list)
    return program_list


def main():
    program_list = "abcde"
    program_list = spin(program_list, 1)
    assert program_list == "eabcd"
    program_list = exchange(program_list, 3, 4)
    assert program_list == "eabdc"
    program_list = partner(program_list, 'e', 'b')
    assert program_list == "baedc"

    program_list = string.ascii_lowercase[:16]
    sequence = load(16).read().split(',')
    program_list = perform_sequence(program_list, sequence)

    print("Solution to part 1: {}".format(program_list))

    program_list = string.ascii_lowercase[:16]
    seen = [program_list]
    for i in range(1, 10**9 + 1):
        program_list = perform_sequence(program_list, sequence)
        if program_list not in seen:
            seen.append(program_list)
        else:
            program_list = seen[10**9 % i]
            break

    print("Solution to part 2: {}".format(program_list))


if __name__ == "__main__":
    main()







