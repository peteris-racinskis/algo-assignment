#!/usr/bin/python3
import sys
import re
from structures import DjSet as st


def process_graph(data):
    vertex_count, edges = get_edges(data)
    result = get_non_positive(edges)
    remaining = get_positive(edges)
    forest = st([])
    for w,u,v in remaining:
        if not forest.same_subset(u,v):
            forest.union(u,v)
        else:
            result.append((w,u,v,))
    print(result)
    print("COST : {}".format(sum(int(w) for w,u,v in result)))
    [print(x) for x in result]
    print(remaining)

def get_positive(edges):
    return list(filter(lambda x: x[0] > 0, edges))

def get_non_positive(edges):
    return list(filter(lambda x: x[0] <= 0, edges))

def get_edges(data):
    vertex_count = data[0]
    data = data[1:]
    edge_number = float(len(data)-1)/3.0
    edges = []
    while len(data) > 0:
        edges.append((
            int(data.pop()),
            int(data.pop()),
            int(data.pop()),
        ))
    edges.sort(key = lambda x: -x[0])
    return vertex_count, edges

def parse_input(path):
    with open(path, 'r') as f:
        d = f.read()
    return list(filter(lambda x: x != "", re.split("\s{1,}", d)))

args = sys.argv
if len(args) > 1:
    filenames = args[1:]
for f in filenames:
    ret = parse_input(f)
    process_graph(ret)
