"""
Time: O(mlg(n))  since m >= n,  m: len(houses)  n: len(heaters)
Space: O(1)


Winter is coming! Your first job during the contest is to design a standard heater with fixed warm radius to warm all the houses.

Now, you are given positions of houses and heaters on a horizontal line, find out minimum radius of heaters so that all houses could be covered by those heaters.

So, your input will be the positions of houses and heaters seperately, and your expected output will be the minimum radius standard of heaters.

Note:
Numbers of houses and heaters you are given are non-negative and will not exceed 25000.
Positions of houses and heaters you are given are non-negative and will not exceed 10^9.
As long as a house is in the heaters' warm radius range, it can be warmed.
All the heaters follow your radius standard and the warm radius will the same.
Example 1:
Input: [1,2,3],[2]
Output: 1
Explanation: The only heater was placed in the position 2, and if we use the radius 1 standard, then all the houses can be warmed.
Example 2:
Input: [1,2,3,4],[1,4]
Output: 1
Explanation: The two heater was placed in the position 1 and 4. We need to use radius 1 standard, then all the houses can be warmed.
"""


import bisect


class Solution(object):
    def findRadius(self, houses, heaters):
        """
        :type houses: List[int]
        :type heaters: List[int]
        :rtype: int
        """
        heaters.sort()
        return max(min(abs(house - heater)
                       for i in [bisect.bisect_right(heaters, house)]  # which heaters this house could use
                       for heater in heaters[i-(i > 0):i+1])
                   for house in houses)


# expanded version
class Solution2(object):
    def findRadius(self, houses, heaters):
        """
        :type houses: List[int]
        :type heaters: List[int]
        :rtype: int
        """
        heaters.sort()
        r = 0
        for house in houses:
            i = bisect.bisect_right(heaters, house)  # which heaters this house could use
            r1 = min(abs(house-heater) for heater in heaters[i-(i>0):i+1])  # find distance to nearest heater
            r = max(r, r1)
        return r