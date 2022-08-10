
############################## Q1 ##########################################
# An increasing run of an integer is a sequence of consecutive digits in which each digit 
# is larger than the last. For example, the number 123444345 has four increasing runs: 
# 1234, 4, 4 and 345. Each run can be indexed from the end of the number, starting with 
# index 0. In the previous example, the 0th run is 345, the first run is 4, the second 
# run is 4 and the third run is 1234.
# 
# Implement get_k_run_starter, which takes in integers n and k and returns the 0th digit 
# of the kth increasing run within n. The 0th digit is the leftmost number in the run. You
# may assume that there are at least k+1 increasing runs in n.
def get_k_run_starter(n, k):
    """
    >>> get_k_run_starter(123444345, 0) # example from description
    3
    >>> get_k_run_starter(123444345, 1)
    4
    >>> get_k_run_starter(123444345, 2)
    4
    >>> get_k_run_starter(123444345, 3)
    1
    >>> get_k_run_starter(123412341234, 1)
    1
    >>> get_k_run_starter(1234234534564567, 0)
    4
    >>> get_k_run_starter(1234234534564567, 1)
    3
    >>> get_k_run_starter(1234234534564567, 2)
    2
    """
    i = 0
    final = None
    while i <= k:
        while n >= 10 and n % 10 > (n // 10) % 10:
            n //= 10
        final = n % 10
        i = i + 1
        n = n // 10
    return final
    # i = 0
    # final = None
    # while ____________________________:
    #     while ____________________________:
    #         ____________________________
    #     final = ____________________________
    #     i = ____________________________
    #     n = ____________________________
    # return final



############################## Q2 ##########################################
# For the purposes of this problem, a score function is a pure function which takes a single 
# number s as input and outputs another number, referred to as the score of s. Complete the 
# best_k_segmenter function, which takes in a positive integer k and a score function score.
# 
# best_k_segmenter returns a function that takes in a single number n as input and returns 
# the best k-segment of n, where a k-segment is a set of consecutive digits obtained by 
# segmenting n into pieces of size k and the best segment is the segment with the highest 
# score as determined by score. The segmentation is right to left.
# 
# For example, consider 1234567. Its 2-segments are 1, 23, 45 and 67 (a segment may be 
# shorter than k if k does not divide the length of the number; in this case, 1 is the 
# leftover, since the segmenation is right to left). Given the score function lambda x: -x, 
# the best 2-segment is 1. With lambda x: x, the best segment is 67.
def best_k_segmenter(k, score):
    """
    >>> largest_digit_getter = best_k_segmenter(1, lambda x: x)
    >>> largest_digit_getter(12345)
    5
    >>> largest_digit_getter(245351)
    5
    >>> largest_pair_getter = best_k_segmenter(2, lambda x: x)
    >>> largest_pair_getter(12345)
    45
    >>> largest_pair_getter(245351)
    53
    >>> best_k_segmenter(1, lambda x: -x)(12345)
    1
    >>> best_k_segmenter(3, lambda x: (x // 10) % 10)(192837465)
    192
    """
    partitioner = lambda x: (x // pow(10, k), x % pow(10, k))
    def best_getter(n):
        assert n > 0
        best_seg = None
        while n > 0:
            n, seg = partitioner(n)
            if best_seg == None or score(seg) > score(best_seg):
                best_seg = seg
        return best_seg
    return best_getter
    # partitioner = lambda x: (________________, ________________)
    # def best_getter(n):
    #     assert n > 0
    #     best_seg = None
    #     while __________________:
    #         n, seg = partitioner(n)
    #         if __________________:
    #             best_seg = seg
    #     return best_seg
    # return best_getter



############################## Q3 ##########################################
# Implement div_by_primes_under, which takes in an integer n and returns an n-divisibility 
# checker. An n-divisibility-checker is a function that takes in an integer k and returns 
# whether k is divisible by any integers between 2 and n, inclusive. Equivalently, it 
# returns whether k is divisible by any primes less than or equal to n.
# 
# Review the Disc 01 is_prime problem for a reminder about prime numbers.
# 
# You can also choose to do the no lambda version, which is the same problem, just with 
# defining functions with def instead of lambda.
def div_by_primes_under(n):
    """
    >>> div_by_primes_under(10)(11)
    False
    >>> div_by_primes_under(10)(121)
    False
    >>> div_by_primes_under(10)(12)
    True
    >>> div_by_primes_under(5)(1)
    False
    """
    checker = lambda x: False
    i = 2
    while i <= n:
        if not checker(i):
            checker = (lambda f, a: lambda x: x % a == 0 or f(x))(checker, i)
        i = i + 1
    return checker

    # checker = lambda x: False
    # i = ____________________________
    # while ____________________________:
    #     if not checker(i):
    #         checker = ____________________________
    #     i = ____________________________
    # return ____________________________


def div_by_primes_under_no_lambda(n):
    """
    >>> div_by_primes_under_no_lambda(10)(11)
    False
    >>> div_by_primes_under_no_lambda(10)(121)
    False
    >>> div_by_primes_under_no_lambda(10)(12)
    True
    >>> div_by_primes_under_no_lambda(5)(1)
    False
    """
    def checker(x):
        return False
    i = 2
    while i <= n:
        if not checker(i):
            def outer(f, a):
                def inner(x):
                    return x % a == 0 or f(x)
                return inner
            checker = outer(checker, i)
        i = i + 1
    return checker
    # def checker(x):
    #     return False
    # i = ____________________________
    # while ____________________________:
    #     if not checker(i):
    #         def outer(____________________________):
    #             def inner(____________________________):
    #                 return ____________________________
    #             return ____________________________
    #         checker = ____________________________
    #     i = ____________________________
    # return ____________________________



############################## Q4 ##########################################
# A k-memory function takes in a single input, prints whether that input was seen exactly k function 
# calls ago, and returns a new k-memory function. For example, a 2-memory function will display 
# “Found" if its input was seen exactly two function calls ago, and otherwise will display “Not found".
# 
# Implement three_memory, which is a three-memory function. You may assume that the value None is never 
# given as an input to your function, and that in the first two function calls the function will display
# “Not found" for any valid inputs given.
def three_memory(n):
    """
    >>> f = three_memory('first')
    >>> f = f('first')
    Not found
    >>> f = f('second')
    Not found
    >>> f = f('third')
    Not found
    >>> f = f('second') # 'second' was not input three calls ago
    Not found
    >>> f = f('second') # 'second' was input three calls ago
    Found
    >>> f = f('third') # 'third' was input three calls ago
    Found
    >>> f = f('third') # 'third' was not input three calls ago
    Not found
    """
    def f(x, y, z):
        def g(i):
            if i == x:
                print("Found")
            else:
                print("Not found")
            return f(y, z, i)
        return g
    return f(None, None, n)
    # def f(x, y, z):
    #     def g(i):
    #         if ____________________________:
    #             ____________________________
    #         else:
    #             ____________________________
    #         return ____________________________
    #     return ____________________________
    # return f(None, None, n)