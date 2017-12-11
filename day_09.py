"""Solution to day 9 parts 1 and 2."""

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def tokenise_stream(stream):
    """Process stream to an array of tokens."""
    return [token for token in stream]

assert tokenise_stream('<>') == ['<', '>']

def process_stream(tokens):
    """Process tokenized stream."""
    groups = {}
    level = 0
    skip_next = False
    in_garbage = False
    for token in tokens:
        if skip_next:
            skip_next = False
            continue
        if token == '!':
            skip_next = True
        elif token == '<' and not in_garbage:
            in_garbage = True
        elif token == '>':
            in_garbage = False
        elif token == '{' and not in_garbage:
            level += 1
        elif token == '}' and not in_garbage:
            groups[level] = (groups.get(level) or 0) + 1
            level -= 1
    return groups

assert process_stream('{}') == {1: 1}

def evaluate_groups_score(groups):
    """Evaluate score of groups."""
    return sum([x * y for x, y in zip(groups.keys(), groups.values())])

# Part 1 test cases
assert evaluate_groups_score(process_stream('{}')) == 1
assert evaluate_groups_score(process_stream('{{{}}}')) == 6
assert evaluate_groups_score(process_stream('{{},{}}')) == 5
assert evaluate_groups_score(process_stream('{{{},{},{{}}}}')) == 16
assert evaluate_groups_score(process_stream('{<a>,<a>,<a>,<a>}')) == 1
assert evaluate_groups_score(process_stream('{{<ab>},{<ab>},{<ab>},{<ab>}}')) == 9
assert evaluate_groups_score(process_stream('{{<!!>},{<!!>},{<!!>},{<!!>}}')) == 9
assert evaluate_groups_score(process_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}')) == 3

# Solution 1 part 1
print('Solution to part 1: {}'.format(
    evaluate_groups_score(process_stream(load(9).read()))))

def find_characters_in_garbage(tokens):
    """Count characters contained within garbage blocks."""
    skip_next = False
    in_garbage = False
    garbage = []
    for token in tokens:
        if skip_next:
            skip_next = False
            continue
        if token == '!':
            skip_next = True
            continue
        elif token == '<' and not in_garbage:
            in_garbage = True
        elif token == '>':
            in_garbage = False
        elif in_garbage:
            garbage.append(token)

    return garbage

# Part 2 test cases
assert len(find_characters_in_garbage(tokenise_stream('<{o"i!a,<{i<a>'))) == 10

# Solution to part 2
print("Solution to part 2: {}".format(
    len(find_characters_in_garbage(
        tokenise_stream(load(9).read())))))
