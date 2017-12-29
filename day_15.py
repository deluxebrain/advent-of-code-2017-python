"""Solution to day 15 parts 1 and 2."""
from math import pow


def generator(seed, factor, divisor, filter_predicate):
    previous_number = seed

    while True:
        previous_number = (previous_number * factor) % divisor
        while not filter_predicate(previous_number):
            previous_number = (previous_number * factor) % divisor
        yield previous_number


def last_16_bits(number):
    binary_representation = "{0:b}".format(number)
    return binary_representation[-16:]


def get_count_of_matches(generator_1, generator_2, attempts):
    matches = 0
    for _ in range(attempts):
        value_1 = next(generator_1)
        value_2 = next(generator_2)
        if last_16_bits(value_1) == last_16_bits(value_2):
            matches += 1
    return matches


def main():
    generator_1 = generator(65, 16807, 2147483647, lambda _: True)
    generator_2 = generator(8921, 48271, 2147483647, lambda _: True)

    # Part 1 test case
    assert get_count_of_matches(generator_1, generator_2, 5) == 1

    generator_1 = generator(516, 16807, 2147483647, lambda _: True)
    generator_2 = generator(190, 48271, 2147483647, lambda  _: True)

    print("Solution to part 1: {}".format(get_count_of_matches(
        generator_1,
        generator_2,
        int(4 * pow(10, 7)))))

    generator_1 = generator(65, 16807, 2147483647, lambda x: x % 4 == 0)
    generator_2 = generator(8921, 48271, 2147483647, lambda x: x % 8 == 0)

    # Part 2 test case
    assert get_count_of_matches(generator_1, generator_2, 1056) == 1

    generator_1 = generator(516, 16807, 2147483647, lambda x: x % 4 == 0)
    generator_2 = generator(190, 48271, 2147483647, lambda x: x % 8 == 0)

    print("Solution to part 2: {}".format(get_count_of_matches(
        generator_1,
        generator_2,
        int(5 * pow(10, 6))
    )))


if __name__ == "__main__":
    main()
