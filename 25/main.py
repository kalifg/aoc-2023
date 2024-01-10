import math
import random
import sys

from shared import input


class Node:
    def __init__(self, name: str):
        self.name: str = name
        self.edges: set[Edge] = set()

    def __repr__(self):
        return f'<{self.name}>'

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Edge:
    def __init__(self, name, u, v):
        self.name = name
        self.nodes: tuple[Node, Node] = (u, v)

    def __repr__(self):
        return f'{self.nodes[0]}-({self.name})-{self.nodes[1]}'

    def __hash__(self):
        return hash(self.name)

    def __call__(self, node: Node):
        if node == self.nodes[0]:
            return self.nodes[1]
        elif node == self.nodes[1]:
            return self.nodes[0]

        return None

    def replace_node(self, u, v):
        if self.nodes[0] == u:
            self.nodes = (v, self.nodes[1])
        elif self.nodes[1] == u:
            self.nodes = (self.nodes[0], v)
        else:
            raise ValueError('Node\'s ({u}) not here man!')


def main(filename: str):
    lines = input.readfile(filename)
    nodes, node_index, edges = process_lines(lines)

    print(f'Graph size: {len(nodes)} nodes')
    print(f'Graph size: {len(edges)} edges')
    print()
    # print_graph(nodes)
    # print()
    # print(graph_groups(nodes))
    # print()

    false_cuts = 0
    minimum_cut = math.inf
    i = 0

    while True:
        i += 1
        print(f'Iteration: {i + 1}')

        nodes, node_index, edges = process_lines(lines)
        karger(nodes, edges)
        # print_graph(nodes)
        potential_cut = [edge.name for edge in edges]

        print(f'Cuts: {len(potential_cut)}')

        nodes, node_index, edges = process_lines(lines)

        for c in potential_cut:
            u, v = c.split(':')
            cut(node_index[u], node_index[v], edges)

        groups = graph_groups(nodes)
        print(groups)
        print(f'Groups: {len(groups)}')
        print()

        if len(groups) != 2:
            false_cuts += 1
        else:
            minimum_cut = min(minimum_cut, len(potential_cut))

        if len(potential_cut) == 3 and len(groups) == 2:
            print(f'Solution found!  Answer = {len(groups[0]) * len(groups[1])}')
            print(f'Cut: {potential_cut}')
            print(f'Minimum cut was {minimum_cut}')
            print(f'False cuts: {false_cuts}')
            break

    # print(graph_edges)
    # print(len(removed_edges), removed_edges)
    # print(graph_groups(graph))


def graph_groups(graph: set[Node]):
    groups = []
    nodes = graph.copy()

    while nodes:
        group = set()
        new_nodes = [nodes.pop()]

        while True:
            next_nodes = set()

            for node in new_nodes:
                group.add(node)
                next_nodes = next_nodes.union((edge(node) for edge in node.edges if edge(node) not in group))

            if not next_nodes:
                break

            new_nodes = next_nodes

        groups.append(group)
        nodes = nodes.difference(group)

    return groups


def cut(u: Node, v: Node, edges: set[Edge]):
    edge: Edge
    node_edges: set[Edge] = set(edge for edge in u.edges if v in edge.nodes)
    node_edges.union((edge for edge in v.edges if u in edge.nodes))

    for edge in node_edges:
        if edge in u.edges:
            u.edges.remove(edge)

        if edge in v.edges:
            v.edges.remove(edge)

        if edge in edges:
            edges.remove(edge)


def karger(graph: set[Node], edges: set[Edge]):
    i = 0

    while True:
        i += 1
        edge = random.choice(list(edges))
        u, v = edge.nodes
        # print(f'{i}: Merging nodes {u} and {v}')
        merge_nodes(u, v, graph, edges)

        if len(graph) < 3:
            break


def print_graph(graph: set[Node]):
    for node in graph:
        print(f'{node} -> {[edge(node) for edge in node.edges]}')

    print()


def process_lines(lines):
    nodes = set()
    node_index = {}
    edges = set()

    for line in lines:
        source, sinks = line.split(': ')
        sinks = sinks.split(' ')

        if source not in node_index:
            node_index[source] = Node(source)

        source = node_index[source]
        nodes.add(source)

        for sink in sinks:
            if sink not in node_index:
                node_index[sink] = Node(sink)

            sink = node_index[sink]
            nodes.add(sink)

            edge = Edge(f'{source.name}:{sink.name}', source, sink)

            source.edges.add(edge)
            sink.edges.add(edge)

            edges.add(edge)

    return nodes, node_index, edges


def merge_nodes(u: Node, v: Node, graph: set[Node], edges: set[Edge]):
    m = Node(f'{u.name}+{v.name}')
    lost_edges = set()

    for edge in u.edges:
        if edge(u) == v:
            lost_edges.add(edge)
            continue

        m.edges.add(edge)
        edge.replace_node(u, m)

    for lost_edge in lost_edges:
        u.edges.remove(lost_edge)
        v.edges.remove(lost_edge)
        edges.remove(lost_edge)

    for edge in v.edges:
        m.edges.add(edge)
        edge.replace_node(v, m)

    graph.remove(u)
    graph.remove(v)
    graph.add(m)


if __name__ == '__main__':
    main(sys.argv[1])
