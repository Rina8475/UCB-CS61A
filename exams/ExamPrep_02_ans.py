############################## Q1 ##########################################
# ! Difficuty: * 
# Implement match_k, which takes in an integer k and returns a function that takes 
# in a variable x and returns True if all the digits in x that are k apart are the 
# same.
# 
# For example, match_k(2) returns a one argument function that takes in x and 
# checks if digits that are 2 away in x are the same.
# 
# match_k(2)(1010) has the value of x = 1010 and digits 1, 0, 1, 0 going from left 
# to right. 1 == 1 and 0 == 0, so the match_k(2)(1010) results in True.
# 
# match_k(2)(2010) has the value of x = 2010 and digits 2, 0, 1, 0 going from left 
# to right. 2 != 1 and 0 == 0, so the match_k(2)(2010) results in False.
# 
# ! RESTRICTION: 
# You may not use strings or indexing for this problem.
# 
# ! IMPORTANT:
# You do not have to use all the lines, one staff solution does not use the line 
# directly above the while loop.
def match_k(k):
    """ Return a function that checks if digits k apart match

    >>> match_k(2)(1010)
    True
    >>> match_k(2)(2010)
    False
    >>> match_k(1)(1010)
    False
    >>> match_k(1)(1)
    True
    >>> match_k(1)(2111111111111111)
    False
    >>> match_k(3)(123123)
    True
    >>> match_k(2)(123123)
    False
    """
    def match_num(x):
        val = x % pow(10, k)
        while x > 0:
            if x % pow(10, k) != val:
                return False
            x //= pow(10, k)
        return True
    return match_num

    # ____________________________
    #     ____________________________
    #     while ____________________________:
    #         if ____________________________:
    #             return ____________________________
    #         ____________________________
    #     ____________________________
    # ____________________________



############################## Q2 ##########################################
# ! Difficulty: **
# For this problem, a chain_function is a higher order function that repeatedly accepts 
# natural numbers (positive integers). The first number that is passed into the function 
# that chain_function returns initializes a natural chain, which we define as a 
# consecutive sequence of increasing natural numbers (i.e., 1, 2, 3). A natural chain 
# breaks when the next input differs from the expected value of the sequence. For 
# example, the sequence (1, 2, 3, 5) is broken because it is missing a 4.
# 
# Implement the chain_function so that it prints out the value of the expected number 
# at each chain break as well as the number of chain breaks seen so far, including the 
# current chain break. Each time the chain breaks, the chain restarts at the most 
# recently input number.
# 
# For example, the sequence (1, 2, 3, 5, 6) would only print 4 and 1. We print 4 
# because there is a missing 4, and we print 1 because the 4 is the first number to 
# break the chain. The 5 broke the chain and restarted the chain, so from here on out 
# we expect to see numbers increasingly linearly from 5. See the doctests for more 
# examples. You may assume that the higher-order function is never given numbers ≤ 0.
# 
# ! IMPORTANT: 
# For this problem, the starter code template is just a suggestion. You are welcome to
# add/delete/modify the starter code template, or even write your own solution that 
# doesn’t use the starter code at all.
def chain_function():
    """
    >>> tester = chain_function()
    >>> x = tester(1)(2)(4)(5) # Expected 3 but got 4, so print 3. 1st chain break, so print 1 too.
    3 1
    >>> x = x(2) # 6 should've followed 5 from above, so print 6. 2nd chain break, so print 2
    6 2
    >>> x = x(8) # The chain restarted at 2 from the previous line, but we got 8. 3rd chain break.
    3 3
    >>> x = x(3)(4)(5) # Chain restarted at 8 in the previous line, but we got 3 instead. 4th break
    9 4
    >>> x = x(9) # Similar logic to the above line
    6 5
    >>> x = x(10) # Nothing is printed because 10 follows 9.
    >>> y = tester(4)(5)(8) # New chain, starting at 4, break at 6, first chain break
    6 1
    >>> y = y(2)(3)(10) # Chain expected 9 next, and 4 after 10. Break 2 and 3.
    9 2
    4 3
    """
    def g(x, y):
        def h(n):
            if n == y + 1:
                return g(x, n)
            else:
                print(y+1, x)
                return g(x+1, n)
        return h
    return lambda x: g(1, x)
    
    # def g(x, y):
    #     def h(n):
    #         if ____________________________:
    #             return ____________________________
    #         else:
    #             ____________________________
    #     return ____________________________
    # return ____________________________



############################## Q3 ##########################################
# ! Difficulty ***
# ! Part A
# Implement cs61nay, which takes a two argument function combiner and positive integer 
# n and returns a function.
# 
# The returned function then takes n arguments, one at a time, and computes 
# combiner(...(combiner(combiner(arg1, arg2), arg3)...), arg_n). Notice combiner takes 
# in two integers and returns one integer.
# 
# For example, the first doctest has the returned function 
# f = cs61nay(lambda x, y: x * y, 3). Now when f is applied to three arguments, like 
# f(2)(3)(4), it multiplies them together, 2*3*4 to get 24.
# 
# ! IMPORTANT
# For this problem, the starter code template is just a suggestion. You are welcome to 
# add/delete/modify the starter code template, or even write your own solution that 
# doesn’t use the starter code at all.
def cs61nay(combiner, n):
    """ Return a function that takes n arguments,
    one at a time, and combines them using combiner.

    >>> f = cs61nay(lambda x, y: x * y, 3)
    >>> f(2)(3)(4) # 2 * 3 * 4
    24
    >>> f(-1)(2)(3) # -1 * 2 * 3
    -6
    >>> f = cs61nay(lambda x, y: x - y, 4)
    >>> f(1)(2)(-2)(-1) # 1 - 2 - -2 - -1
    2
    >>> f = cs61nay(lambda x, y: x + y, 1)
    >>> f(61)
    61
    >>> f(2021)
    2021
    """
    def func(a, b):
        if b == 0:
            return a
        return lambda x: func(combiner(a, x), b-1)
    return lambda x: func(x, n-1)

    # if ____________________________:
    #     return ____________________________
    # else:
    #     return ____________________________

# ! Difficulty ***
# ! Part B
# Somebody who writes very complicated code has given you a challenge! You would hopefully 
# never see something so hard to comprehend in the real world.
# 
# Complete the expression below by writing one integer in each blank so that the whole 
# expression evaluates to 2021. Assume cs61nay is implemented correctly.
from operator import sub, add, mul

compose = lambda f, g: lambda x: f(g(x))

print(compose(cs61nay(sub, 2), compose(cs61nay(mul, 3)(2),
      cs61nay(pow, 2)(10))(3))(1)(-21))
# print(compose(cs61nay(sub, ____), compose(cs61nay(mul, ____)(2),
#       cs61nay(pow, 2)(10))(3))(____)(____))

# ! Difficulty **
# ! Part C
# All those lines of code are unnecessary! Solve cs61NAY but only using one line.
# ! RESTRICTION: 
# You may not use the python ternary operator (the one line if/else statment).

cs61NAY = lambda f, x: cs61nay(f, x)        # I'm not sure if this is right

# This syntax adds a doctest to a lambda, which can be run using `test(cs61NAY)`
# after clicking Run in 61A Code or `python3 -m doctest -v examprep02.py`
# if you save the questions to a .py file
cs61NAY.__name__ = "cs61NAY"
cs61NAY.__doc__ = """ Return a function that takes n arguments,
    one at a time, and combines them using combiner.

    >>> f = cs61NAY(lambda x, y: x * y, 3)
    >>> f(2)(3)(4) # 2 * 3 * 4
    24
    >>> f(-1)(2)(3) # -1 * 2 * 3
    -6
    >>> f = cs61NAY(lambda x, y: x - y, 4)
    >>> f(1)(2)(-2)(-1) # 1 - 2 - -2 - -1
    2
    >>> f = cs61NAY(lambda x, y: x + y, 1)
    >>> f(61)
    61
    >>> f(2021)
    2021
    """



############################## Q3 ##########################################
# ! Part A
# Implement the following higher order functions so that we can simulate append and get behavior. 
# As the name suggests, the get function should get the ith element that was appended (the first 
# element that was appended is element 0). For example, if I append 2, append 30, and then append 
# 4, then get(0) is 2 (the first element appended), get(1) is 30 (the second element appended), 
# and get(2) is 4 (the third element appended). If I append more items, get(0) through get(2) 
# should not be affected. Assume all get calls ask for non-negative indices (i.e., you’d never do 
# get(-1)). If the argument to get would go out of bounds otherwise, the call should return the 
# string "Error: out of bounds!".
# 
# ! RESTRICTION: 
# you are not allowed to use any lists / sets / dictionaries / iterators, or any other data 
# structures.
def stacklist():
    """
    >>> append, get = stacklist()
    >>> get, y = append(2)
    >>> get, y = append(3, get, y)
    >>> get, y = append(4, get, y)
    >>> get(0)
    2
    >>> get(1)
    3
    >>> get(2)
    4
    >>> get, y = append(8, get, y)
    >>> get(1)
    3
    >>> get(3)
    8
    """
    g = lambda i: "Error: out of bounds!"
    def f(value, g=g, y=0):
        h = g
        def g(i):
            if i == y:
                return value
            return h(i)
        return (g, y+1)
    return f, g
    
    # g = lambda i: "Error: out of bounds!"
    # def f(value, g=g, y=____________________________):
    #     ____________________________
    #     def g(i):
    #         if ____________________________:
    #             return ____________________________
    #         return ____________________________
    #     return ____________________________
    # return f, g

# ! Part B
# Build on your solution to the previous question to implement insert functionality! As the name 
# suggests, the insert function inserts a value into an existing sequence of numbers. The function 
# takes an insertion index, the value to insert into that index, as well as two other arguments 
# whose purpose is left for you to determine. When the value is inserted into the provided index, 
# all numbers from that index and to the right are shifted one element right. For example, if my 
# current sequence is 5, 9, 14, 3 and I specify an insertion index of 1 with value 100, then my 
# updated sequence should be 5, 100, 9, 14, 3. The 100 is inserted at index 1, and all numbers 
# from the original index 1 to the end are shifted to the right by one position. You can always 
# assume that the provided insertion index will be within bounds.
# 
# You don’t actually have to represent the sequence as a contiguous block of numbers that need 
# to shift around though. As long as the get(i) call returns the correct value, that’ll do.
# 
# ! RESTRICTION: 
# You are not allowed to use any lists / dictionaries / iterators, or any other data structures.
def stacklisted():
    """
    >>> append, get, insert = stacklisted()
    >>> get, idx = append(2)
    >>> get, idx = append(13, get, idx)
    >>> get, idx = append(4, get, idx)
    >>> get, idx = insert(1, 19, get, idx)
    >>> get(0)
    2
    >>> get(1)
    19
    >>> get(2)
    13
    >>> get(3)
    4
    """
    g = lambda i: "Error: out of bounds!"
    def f(value, g=g, y=0):
        h = g
        def g(i):
            if i == y:
                return value
            return h(i)
        return (g, y+1)
    
    def h(y, value, g, n):
        e = g
        def g(i):
            if i == y:
                return value
            return e(i)
        k = y
        while k < n:
            g, ret = f(e(k), g, k+1)
            k += 1
        return g, ret
    return f, g, h
    # Assume f and g are defined correctly from the previous question
    # def h(y, value, g, n):
    #     e = ____________________________
    #     def g(i):
    #         if ____________________________:
    #             return ____________________________
    #         return ____________________________
    #     k =____________________________
    #     while k < ____________________________:
    #         g, ret = f(______,_______________________,______)
    #         k += 1
    #     return g, ret
    # return f, g, h