#!/usr/bin/python3

class DjNode:

    def __init__(self, x):
        self.x = x
        self.parent = None
        self.size = 1
    
    def __repr__(self):
        return "Node({}, {}, {})".format(self.x, self.parent, self.size)

    def get_root(self):
        if self.parent:
            root = self.parent.get_root()
            self.update_parent(root)
            return root
        return self

    def update_parent(self, y):
        self.parent = y
    
    def get_size(self):
        return self.size

    def add_size(self, x):
        self.size = self.size + x


"""

Methods:
    
    find_root(x): 
    - returns x if parent(x) is x
    - returns find_root(parent(x)) if x is not own parent
    - updates parent(x) to find_root(x)
    
    union(x,y):
    - checks if find_root same for x, y
    - if not, compare number of children for each root
    - parent(smaller) <- bigger
    - children(bigger) = children(smaller) + children(bigger)

"""


class DjSet:

    def __init__(self, iterable):
        self._nodes = {x:DjNode(x) for x in iterable}

    def __repr__(self):
        return "Disjoint Set: {} ".format(self._nodes)
        
    def find_root(self, x):
        if x not in self._nodes:
            self._nodes[x] = DjNode(x)
        return self._nodes[x].get_root()

    def same_subset(self, x, y):
        return self.find_root(x).x == self.find_root(y).x

    def union(self, x, y):
        if self.same_subset(x,y):
            return
        roots = [self._nodes[x].get_root(), self._nodes[y].get_root()]
        roots.sort(key = lambda x: x.get_size())
        roots[0].update_parent(roots[1])
        roots[1].add_size(roots[0].get_size())
        

