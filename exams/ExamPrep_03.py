############################## Q1 ##########################################
# ! Difficulty: *
# A palindrome is a string that remains identical when reversed. Given a string s, is_palindrome 
# should return whether or not s is a palindrome.
#
# ! IMPORTANT:
# Please use the template for this problem; if you have spare time, try to solve the problem using 
# iteration without the template.
def is_palindrome(s):
    """
    >>> is_palindrome("tenet")
    True
    >>> is_palindrome("tenets")
    False
    >>> is_palindrome("raincar")
    False
    >>> is_palindrome("")
    True
    >>> is_palindrome("a")
    True
    >>> is_palindrome("ab")
    False
    """
    if len(s) <= 1:
        return True
    return is_palindrome(s[1:-1]) and s[0] == s[-1]
    # if _____________________________________________________________:
    #     return True
    # return _________________________________________________________



############################## Q2 ##########################################
# ! Difficulty **
# A substring of s is a sequence of consecutive letters within s. Given a string s, greatest_pal should 
# return the longest palindromic substring of s. If there are multiple palindromic substrings of greatest 
# length, then return the leftmost one. #? You may use is_palindrome.
# 
# ! IMPORTANT: 
# For this problem, each starter code template is just a suggestion. We recommend that you use the first, 
# but feel free to modify it, try one of the other two or write your own if you'd like to. Comment out 
# the other versions of the function to run doctests.
def greatest_pal(s):
    """
    >>> greatest_pal("tenet")
    'tenet'
    >>> greatest_pal("tenets")
    'tenet'
    >>> greatest_pal("stennet")
    'tennet'
    >>> greatest_pal("25 racecars")
    'racecar'
    >>> greatest_pal("abc")
    'a'
    >>> greatest_pal("")
    ''
    """
    if is_palindrome(s):
        return s
    left, right = greatest_pal(s[0:-1]), greatest_pal(s[1:])
    return left if len(left) >= len(right) else right

    # if ______________________________________________________:
    #     return s
    # left, right = _________________________________________________________
    # if ___________________________________________________________________________:
    #     return ____________________________________________________________________
    # return ____________________________________________________________________



############################## Q3 ##########################################
# ! Difficulty ***
def greatest_pal_two(s):
    """
    >>> greatest_pal_two("tenet")
    'tenet'
    >>> greatest_pal_two("tenets")
    'tenet'
    >>> greatest_pal_two("stennet")
    'tennet'
    >>> greatest_pal_two("abc")
    'a'
    >>> greatest_pal_two("")
    ''
    """
    # for _____ in __________________________________________________________:
    #     if ________________________________________________________________________:
    #         return  ________________________________________________________________________
    # return s
