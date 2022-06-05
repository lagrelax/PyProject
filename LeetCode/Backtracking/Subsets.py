from utils import *

class Solution:

    def __init__(self):
        self.path = []
        self.res = []

    def subsets(self, nums: List[int]) -> List[List[int]]:

        self.res.append([])
        self.backtracking(nums, 0)

        return self.res

    def backtracking(self, nums, idx):

        if idx >= len(nums):
            return

        for i in range(idx, len(nums)):
            new_set = nums[i]
            self.path.append(new_set)
            if self.path not in self.res:
                # Note to do a deep copy here
                self.res.append(self.path[:])
            self.backtracking(nums, i + 1)
            self.path.pop()

if __name__ == '__main__':
    sol = Solution()
    input = [1,2,3]
    print(sol.subsets(input))

