"""Solution to day 17 parts 1 and 2"""


def rotate(diameter, cursor, steps):
    return ((cursor + steps) % diameter) + 1


assert rotate(1, 0, 3) == 1
assert rotate(2, 1, 3) == 1
assert rotate(3, 1, 3) == 2


def spin(spinlock, cursor, number):
    return spinlock[:cursor] + [number] + spinlock[cursor:]


assert spin([0], 1, 1) == [0, 1]
assert spin([0, 1], 1, 2) == [0, 2, 1]


def execute_spinlock_iterations(spinlock, cursor, steps, iterations):
    for number in range(1, iterations + 1):
        cursor = rotate(len(spinlock), cursor, steps)
        spinlock = spin(spinlock, cursor, number)

    return spinlock, cursor


def main():
    spinlock, cursor = execute_spinlock_iterations([0], 0, 3, 2017)
    assert spinlock[rotate(len(spinlock), cursor, 0)] == 638

    spinlock, cursor = execute_spinlock_iterations([0], 0, 377, 2017)
    print("Solution to part 1: {}".format(spinlock[rotate(len(spinlock), cursor, 0)]))

    cursor = 0
    value_after_zero = 0
    for number in range(1, 50000000 + 1):
        cursor = rotate(number, cursor, 377)
        if cursor == 1:
            value_after_zero = number

    print("Solution to part 2: {}".format(value_after_zero))


if __name__ == "__main__":
    main()
