############################## Q1 ##########################################
# ! Difficulty
def sum_tree(t):
    """
    Add all elements in a tree.

    >>> t = Tree(4, [Tree(2, [Tree(3)]), Tree(6)])
    >>> sum_tree(t)
    15
    """
    "*** YOUR CODE HERE ***"
    return sum([sum_tree(x) for x in t.branches], start=t.label)

def equal(lst):
    """Receive a list, if all the element in the list are equal to each other,
    Return True, else return False"""
    if lst == []:
        return True
    first = lst[0]
    return all([first == x for x in lst])

def balanced(t):
    """
    Checks if each branch has same sum of all elements,
    and each branch is balanced.

    >>> t = Tree(1, [Tree(3), Tree(1, [Tree(2)]), Tree(1, [Tree(1), Tree(1)])])
    >>> balanced(t)
    True
    >>> t = Tree(t, [t, Tree(1)])
    >>> balanced(t)
    False
    """
    "*** YOUR CODE HERE ***"
    return all([balanced(x) for x in t.branches]) and equal([sum_tree(x) for x in t.branches])
    

def prune_tree(t, predicate):
    """
    Returns a new tree where any branch that has the predicate of the label
    of the branch returns True has its branches pruned.

    >>> prune_tree(Tree(1, [Tree(2)]), lambda x: x == 1) # prune at root
    [1]
    >>> prune_tree(Tree(1, [Tree(2)]), lambda x: x == 2) # prune at leaf
    [1, [2]]
    >>> prune_tree(test_tree, lambda x: x >= 3) # prune at 3, 4, and 5
    [1, [2, [4], [5]], [3]]
    >>> sum_tree(prune_tree(test_tree, lambda x: x > 10)) # prune nothing, add 1 to 9
    45
    >>> prune_tree(test_tree, lambda x: x > 10) == test_tree # prune nothing
    True
    """
    "*** YOUR CODE HERE ***"
    if predicate(t.label):
        return Tree(t.label, [prune_tree(x) for x in t.branches if prune_tree(x) is not None])

# test_tree = Tree(1,
#                 [Tree(2,
#                     [Tree(4,
#                         [Tree(8),
#                             Tree(9)]),
#                     Tree(5)]),
#                 Tree(3,
#                     [Tree(6),
#                     Tree(7)])])
# draw(test_tree)


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