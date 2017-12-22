"""Solution to day 12 parts 1 and 2."""
import re

TEST_CASE="""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename)

def parse_graph_node(raw):
    """Parse raw node representation to node data structure."""
    node, connections = re.match(r'(\d+)(?: <-> )(.+)', raw).groups()
    return int(node), map(int, connections.split(', '))

assert parse_graph_node('2 <-> 0, 3, 4') == (2, [0, 3, 4])

def parse_graph(raw):
    """Parse raw graph representation to graph data structure."""
    return {a: b
        for (a, b) in [parse_graph_node(line)
        for line in raw.splitlines()]}

assert parse_graph(TEST_CASE) == {
    0: [2],
    1: [1],
    2: [0, 3, 4],
    3: [2, 4],
    4: [2, 3, 6],
    6: [4, 5],
    5: [6],
}

def find_path(graph, start, end, path = None):
    """Find 1 of the possibly paths between the start and the end nodes."""
    if not path:
        path = []

    path = path + [start]

    if start == end:
        return path

    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath

    return None

assert find_path(parse_graph(TEST_CASE), 0, 6) == [0, 2, 3, 4, 6]

def find_connected_nodes(graph, connection):
    """List nodes connected to specified node."""
    return [node for node in graph if find_path(graph, node, connection)]

# Part 1 test case
assert len(find_connected_nodes(parse_graph(TEST_CASE), 0)) == 6

print("Solution to part 1: {}".format(
    len(
        find_connected_nodes(
            parse_graph(load(12).read()), 0))))

def connected_group(graph, start, connected = None):
    """Find all nodes that are connected to the specified node."""
    if not connected:
        connected = []

    if start in connected:
        return connected

    connected.append(start)

    for node in graph[start]:
        connected = connected_group(graph, node, connected)

    return connected

def find_groups(graph):
    """Find all groups within the graph."""
    groups = set()
    for node in graph.keys():
        groups.add(frozenset(connected_group(graph, node)))

    return groups

assert len(find_groups(parse_graph(TEST_CASE))) == 2

print("Solution to part 2: {}".format(len(find_groups(parse_graph(load(12).read())))))