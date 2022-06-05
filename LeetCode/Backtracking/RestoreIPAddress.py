from utils import *


class Solution:
    def __init__(self):
        self.path = []
        self.res = []
        self.numPoint = 0

    def restoreIpAddresses(self, s: str) -> List[str]:

        if len(s) < 4:
            return []

        self.backtracking(s, 0)
        return self.res

    def backtracking(self, s, idx):

        if idx >= len(s):
            if self.path[-1] != '.':
                self.res.append(''.join(self.path))
            return

        for i in range(idx, len(s)):
            new_s = s[idx:i+1]
            if self.isValid(new_s) and self.numPoint < 4:
                self.path.append(new_s)
                if self.numPoint < 3:
                    self.path.append('.')
                self.numPoint += 1
                self.backtracking(s, i+1)
                if self.path[-1] == '.':
                    self.path.pop()
                self.numPoint -= 1
                self.path.pop()


    def isValid(self, s):
        if len(s) > 1 and s[0] == '0':
            return False

        if int(s) > 255:
            return False

        return True


if __name__ == '__main__':
    input = "101023"
    sol = Solution()
    print(sol.restoreIpAddresses(input))

