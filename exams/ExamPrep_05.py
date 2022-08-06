############################## Q1 ##########################################
# ! Difficulty **
def node_printer(t):
    """
    >>> t1 = Tree(1, [Tree(2,
    ...                   [Tree(5),
    ...                    Tree(6, [Tree(8)])]),
    ...               Tree(3),
    ...               Tree(4, [Tree(7)])])
    >>> printer = node_printer(t1)
    >>> for _ in range(8): # NOTE: it's okay to fail this test if all 8 are printed once
    ...     printer()
    1
    2
    3
    4
    5
    6
    7
    8
    """
    to_explore = [t]
    def step():
        node = to_explore.pop(0)
        to_explore.extend(node.branches)
        print(node.label)
    return step



############################## Q2 ##########################################
# ! Difficulty **
def fib_gen():
    """
    >>> fg = fib_gen()
    >>> for _ in range(7):
    ...     print(next(fg))
    0
    1
    1
    2
    3
    5
    8
    """
    # yield from __________________________________
    # a = __________________________________________
    # ______________________________________________
    # for x, y in __________________________________:
    #     ___________________________________________
    a, b = 0, 1
    yield from [a, b]
    while True:
        a += b
        a, b = b, a
        yield b



############################## Q4 ##########################################
# ! Difficulty ***
def partition_gen(n):
    """
    >>> for partition in partition_gen(4): # note: order doesn't matter
    ...     print(partition)
    [4]
    [3, 1]
    [2, 2]
    [2, 1, 1]
    [1, 1, 1, 1]
    """
    def yield_helper(j, k):
        if j == 0:
            yield []
        elif not (k == 0 or j < 0):
            for small_part in yield_helper(j-k, k):
                yield [k] + small_part
            yield from yield_helper(j, k-1)
    yield from yield_helper(n, n)



############################## Q4 ##########################################
# ! Difficulty *
def amplify(f, x):
    """Yield the longest sequence x, f(x), f(f(x)), ... that are all true values

    >>> list(amplify(lambda s: s[1:], 'boxes'))
    ['boxes', 'oxes', 'xes', 'es', 's']
    >>> list(amplify(lambda x: x//2-1, 14))
    [14, 6, 2]
    """
    "*** YOUR CODE HERE ***"
    while x:
        yield x
        x = f(x)



class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()