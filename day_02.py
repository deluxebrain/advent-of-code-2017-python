"""Solution to day 2 parts 1 and 2"""
import re

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename).read()

def parse_ints(text):
    """Form a list from all the integers in the text"""
    return [int(x) for x in re.findall(r'\d+', text)]

def calculate_row_checksum(row):
    """Form the row checksum as the difference between
    the largest and the smallest row items"""
    sorted_row = sorted(row)[0]
    smallest, largest = sorted_row, sorted(row)[-1]
    return largest - smallest

def calculate_document_checksum(doc):
    """Form the document checksum as the sum of all row checksums"""
    rows = [parse_ints(row) for row in doc.splitlines() if row.strip()]
    return sum(map(calculate_row_checksum, rows))

assert parse_ints('1 2 3') == [1, 2, 3]
assert calculate_row_checksum(parse_ints('5 1 9 5')) == 8

# Part 1 test case
EXAMPLE_DOC_1 = ("""
    5 1 9 5
    7 5 3
    2 4 6 8
""")
assert calculate_document_checksum(EXAMPLE_DOC_1) == 18

# Part 1 solution
print("Solution to part 1: {}".format(calculate_document_checksum(load(2))))

def form_pairs(row, pairs=None):
    """Form all combinations of pairs in a list"""
    if pairs is None:
        pairs = []
    if row == []:
        return pairs

    head, rest = row[0], row[1:]
    for value in rest:
        pairs.append(sorted([head, value], reverse=True))
    return form_pairs(rest, pairs)

assert form_pairs([1, 2, 3]) == [[2, 1], [3, 1], [3, 2]]

def is_evenly_divisible(pair):
    """Evaluates if pair is evenly divisible"""
    return not pair[0] % pair[1]

assert not is_evenly_divisible([3, 2])
assert is_evenly_divisible([8, 4])

def calculate_row_checksum_ex(row):
    """Form the row checksum as the division of the only
    two evenly divisible numbers"""
    pairs = [pair for pair in form_pairs(row) if is_evenly_divisible(pair)]
    return int(pairs[0][0] / pairs[0][1])

assert calculate_row_checksum_ex([5, 9, 2, 8]) == 4

def calculate_document_checksum_ex(doc, checksum_strategy):
    """Form the document checksum as the sum of all row checksums"""
    rows = [parse_ints(row) for row in doc.splitlines() if row.strip()]
    return sum(map(checksum_strategy, rows))

# Part 2 test case
EXAMPLE_DOC_2 = ("""
    5 9 2 8
    9 4 7 3
    3 8 6 5
""")

assert calculate_document_checksum_ex(EXAMPLE_DOC_2, calculate_row_checksum_ex) == 9

# Solution to part 2
print("Solution to part 2: {}".format(
    calculate_document_checksum_ex(
        load(2), calculate_row_checksum_ex)))
