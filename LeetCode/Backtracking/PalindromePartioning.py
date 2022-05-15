from utils import *

class Solution:

    def __init__(self):

        self.path = []
        self.res = []

    def partition(self, s: str) -> List[List[str]]:

        if len(s) == 1:
            return [[s]]

        self.backtracking(s, 0)
        return self.res

    def backtracking(self, s: str, idx: int):

        if idx >= len(s):
            self.res.append(self.path[:])
            return

        # idx starts with 0
        sub = ''
        for i in range(idx, len(s)):
            sub = s[idx: i+1]
            if sub == sub[::-1]:
                self.path.append(sub)
                self.backtracking(s, i + 1)
                self.path.pop()

        return True
if __name__ == '__main__':
    input = 'cdd'
    sol = Solution()
    res = sol.partition(input)
    print(res)