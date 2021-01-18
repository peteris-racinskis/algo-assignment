#!/usr/bin/python3
import sys
import re
from structures import DjSet as st


"""
Main program loop
"""
def process_graph(data):
    edges = get_edges(data)
    result = get_non_positive(edges)
    remaining = get_positive(edges)
    remaining.sort(key = lambda x: -x[0])
    forest = st([])
    for w,u,v in remaining:
        if not forest.same_subset(u,v):
            forest.union(u,v)
        else:
            result.append((w,u,v,))
    count = len(result)
    total_cost = sum(int(w) for w,_,_ in result)
    return count, total_cost, result

def get_positive(edges):
    return list(filter(lambda x: x[0] > 0, edges))

def get_non_positive(edges):
    return list(filter(lambda x: x[0] <= 0, edges))

def get_edges(data):
    data = data[1:]
    edges = []
    while len(data) > 0:
        edges.append((
            int(data.pop()),
            int(data.pop()),
            int(data.pop()),
        ))
    return edges

def parse_input(path):
    with open(path, 'r') as f:
        d = f.read()
    return list(filter(lambda x: x != "", re.split("\s{1,}", d)))

def print_to_file(k,w,res,filename):
    s = "{}\t{}\t".format(k,w)
    for r in res:
        s = s + "\t{}\t{}".format(r[1],r[2])
    with open(filename, 'w') as f:
        f.write(s)
        f.write("\n")


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        output = args[2]
    else:
        output = "output.txt"
    if len(args) > 1:
        filename = args[1]
        f = parse_input(filename)
        k, w, res = process_graph(f)
        print_to_file(k,w,res,output)
        print("Number of stashes: {}".format(k))
        print("Cost of stashes:   {}".format(w))
    
