"""Solution to day 7 parts 1 and 2."""
import re

TOWER = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def parse_line(line):
    """Parse single line in tower."""
    # \w character
    # \d digit
    # \s whitespace
    # (...) group
    # (?:...) non-capturing group
    # ? optional
    name, weight, children = re.match(r'(\w+)\s\((\d+)\)(?: -> )?(.+)?', line).groups()
    children = re.findall(r'\w+', children or '')
    return name, int(weight), children

def parse_tower(tower):
    """Parse tower into dictionary."""
    program_weights = {}
    program_tree = {}

    for line in tower.splitlines():
        name, weight, children = parse_line(line)
        program_weights[name] = weight
        for child in children or []:
            program_tree[child] = name

    # There is no node that has the root node as a child
    # Hence it will be missing from the program tree
    root_programs = (program_weights.keys() - program_tree.keys())
    root_program = list(root_programs)[0]
    program_tree[root_program] = None

    return program_tree, program_weights

def find_root_node(program_tree):
    """Find root program."""
    return [program for program in program_tree if not program_tree[program]][0]

# Part 1 test cases
assert find_root_node(parse_tower(TOWER)[0]) == 'tknk'

# Part 1 solution
print("Solution to part 1: {}".format(find_root_node(parse_tower(load(7).read())[0])))

def invert_tree(parent_view_tree):
    """Convert from parent view to child view."""
    child_view_tree = {}
    for child in parent_view_tree:
        parent = parent_view_tree[child]
        if parent:
            child_view_tree[parent] = child_view_tree[parent] \
                if parent in child_view_tree else set()
            child_view_tree[parent].add(child)
    return child_view_tree

def calcuate_aggregated_weights(program_tree, program_weights, node):
    """Calculate the aggregated weights for each node and all child nodes."""
    aggregated_weights = {}

    def walk_tree(node):
        """Walk the tree from the bottom up"""
        aggregated_weights[node] = aggregated_weights[node] \
            if node in aggregated_weights else program_weights[node]

        if node not in program_tree:
            return

        for child_node in program_tree[node]:
            walk_tree(child_node)
            aggregated_weights[node] += aggregated_weights[child_node]

        return aggregated_weights

    return walk_tree(node)

def find_unbalanced_program(program_tree, aggregated_weights):
    """Find the node in the tree that is unbalanced."""
    # Find all the nodes that are candidates to be unbalanced.
    # I.e. all nodes that have child nodes
    parent_nodes = set(parent_node for parent_node in program_tree.values() if parent_node)
    unbalanced_nodes = {}

    # For all candidate nodes, look at the aggregated weights of all its
    # direct children
    for parent_node in parent_nodes:
        weights = sorted([aggregated_weights[child_node] \
            for child_node in program_tree.keys() \
                if program_tree[child_node] == parent_node], reverse=True)
        if weights[0] != weights[-1]:
            # Store off the unbalanced node and its parent node
            unbalanced_nodes[parent_node] = program_tree[parent_node]

    # As there is only one unbalanced node, the list of unbalanced nodes
    # must form a subtree. The actual unbalanced node is lowest node -
    # i.e the node that no other nodes in the subtree are pointing to
    unbalanced_node = [unbalanced_node for unbalanced_node in unbalanced_nodes \
        if unbalanced_node not in unbalanced_nodes.values()][0]

    return unbalanced_node

def find_badly_weighted_node(inverted_program_tree, aggregated_weights, program):
    """Given an unbalanced program, return the child node and
    weight adjustment required to balance the node."""
    child_weights = [aggregated_weights[child_node] \
        for child_node in inverted_program_tree[program]]
    weight_counts = {weight: child_weights.count(weight) for weight in child_weights}
    weights, counts = weight_counts.keys(), weight_counts.values()

    # Sort weights into list ordered desc by their frequency
    # I.e. the first weight will be the common weight
    # The last weight will be the incorrect weight
    sorted_weights = [weight for _, weight in sorted(zip(counts, weights), reverse=True)]

    # Find the bad node by looking it up based on its incorrect weight
    unbalanced_node = [node for node in inverted_program_tree[program] \
        if aggregated_weights[node] == sorted_weights[-1]][0]

    # Return the badly weights node and the correction required to its weight
    return unbalanced_node, sorted_weights[0] - sorted_weights[-1]

def find_correct_weight(program_weights, program, correction):
    """Return new weight for node."""
    return program_weights[program] + correction

def solve_for_part_2():
    """Wrapper function for part 2."""
    program_tree, program_weights = parse_tower(load(7).read())
    root_node = find_root_node(program_tree)
    inverted_program_tree = invert_tree(program_tree)
    aggregated_weights = calcuate_aggregated_weights(
        inverted_program_tree, program_weights, root_node)
    unbalanced_program = find_unbalanced_program(program_tree, aggregated_weights)
    return find_correct_weight(
        program_weights, *find_badly_weighted_node(
            invert_tree(program_tree), aggregated_weights, unbalanced_program))

print("Solution to part 2: {}".format(solve_for_part_2()))
