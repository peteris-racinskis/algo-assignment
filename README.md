# Homework solution - complement of max spanning forest using Kruskal's algorithm

Finds the complement (set of discarded edges) of the max spanning forest of the provided input data after all edges of weight less than or equal to 0 have been removed.

### Installation and usage

No packaging provided, but since the tool requires no external libraries, cloning this repository on any machine with Python 3.6+ should suffice:

```
$ https://github.com/peteris-racinskis/algo-assignment.git
$ cd algo-assignment/
$ ./main.py <input file> [<output file>]

```

Default output file location:

```
./output.txt

```

## Description of the program 

Since this is a homework assignment dealing with asymptotic complexity and not a piece of production code, no attempt toward optimizing real runtime performance has been made. Hashmap type datastructures are native to Python and have approximately O(1) time complexity for insert/lookup operations, so they've been used without regard to the (oftentimes very large) constant factor penalties when compared to linear search operations (which can be very fast on modern CPU hardware).

#### How it works

1. Input file is read into a string, split into blocks of non-whitespace text using regular expressions; empty substrings are removed and remaining elements are cast to integer type. O(m)
2. Resulting Python list (dynamic array/linked list) of integers is organized into a list of tuples from the top (using n * O(1) list.pop() operations), representing graph edges. O(m)
3. Two lists are created - result and remaining. All edges with weight <= 0 are copied into the result list, while the others are copied into the remaining list. O(m)
4. The "remaining" list is sorted in decreasing order by weight of each edge. O(m log m)
5. A Disjoint Set datastructure (with custom implementation) is created to contain the vertices and may or may not be initialized (depending on what the author has finally decided on in the final commit before sharing this assignment). (somewhere in the O(1 ... n) region)
6. Iteration over all the edges in the "remaining" list, starting from the largest. Disjoint Set representing a forest of trees is used to determine if the two vertices already belong to the same tree in the forest. If not, the trees both vertices belong to are joined into a single tree. If yes, no action is performed on the disjoint set but the edge is appended to the "result" list. See COMPLEXITY OF DISJOINT SET OPERATIONS below for details.
7. The length of the "result" list is returned as the number of stashes that need to be created. O(1)
8. The sum of the weights of all edges in the "result" list is computed. O(m)
9. Results are formatted and output to file. ~O(m)

#### Complexity of Disjoint Set operations

The idea for this data structure as well as its implementation details were derived from the following Wikipedia articles:

[Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

[Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)

The data structure in this case is implemented using a Python dictionary, which is itself a hashmap-type data structure whose underlying implementation is an array of hashes, keys and value pointers. According to language documentation, average amortized time complexity for insertion, deletion and lookup operations can be expected to be O(1). However, this is at the expense of periodic resize operations which can have wildly varying constant time delay. Furthermore, the nature of using reference data types as the values in the dictionary, along with Python's hidden memory allocation and managament system means that it's difficult to predict what memory access time penalties might be incurred at runtime. 

When optimizing for real time performance, it's quite possible that using simpler list/array types would net performance benefits, but that would require looking past the high-level abstractions provided by the language and diving into implementation details.

The values corresponding to integer keys in the disjoint set are represented by instances of the DjNode class, which contains a value (type agnostic), a size variable (integer) and a reference to a parent object (null or another instance of the same class). They expose constant time get_size(), add_size() and update_parent() methods, which operate on the fields of the object, as well as a recursive get_root() method which is called on the parent objects until one with no parent is found. This is then made the parent of all instances in the call stack on the return pass to implement so called "path compression". This operation ensures that the tree stays relatively flat, and few calls are required to reach the root object on each lookup operation. This is one of the methods whereby asymptotically optimal time complexity can be achieved - a(n) (for a DjSet of size n) where a is the inverse Ackerman function (almost constant).

The DjSet class itself exposes the following methods - find_root(), same_subset() and union() - all of which employ the find_root() method of the DjNode class and therefore share the same asymptotic complexity.

Combining everything so far: each call of union() or same_subset() from the main program execution loop has an estimated amortized time complexity of O(a(n)), where a - the inverse Ackerman function. This can be in practical terms be thought of as roughly equivalent to O(1) or far less than O(log n).
