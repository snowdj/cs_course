"""
Time: O(n)
Space: O(1), or O(n) if using hash table.

Given two strings s and t which consist of only lowercase letters.

String t is generated by random shuffling string s and then add one more
letter at a random position.

Find the letter that was added in t.

Example:

Input:
s = "abcd"
t = "abcde"

Output:
e

Explanation:
'e' is the letter that was added.
"""


# Same as 136 single number.
class Solution:
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        ans = 0
        for c in s+t:
            ans ^= ord(c)
        return chr(ans)


class Solution2:
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        ans = 0
        for c in s:
            ans -= ord(c)
        for c in t:
            ans += ord(t)
        return chr(ans)


# write solution 1 to one line
import functools
import operator


class Solution3:
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        return chr(functools.reduce(operator.xor, map(ord, s+t)))