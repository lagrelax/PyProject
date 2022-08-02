from typing import *
import collections


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        res = collections.deque([nums[0]])
        for x in nums[1:]:
            while res and x > res[-1]:
                res.pop()
            if len(res) <= k:
                res.append(x)
        return res[k-1]

if __name__ == '__main__':
    input = [3,2,1,5,6,4]
    k = 2
    sol = Solution()
    res = sol.findKthLargest(input,2)
    print(res)
