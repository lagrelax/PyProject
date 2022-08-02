from utils import *

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        if len(s) == 0:
            return s
        if len(s) == 1:
            if s[0] not in ['(',')']:
                return s
            else:
                return ""

        stk = []
        for i, x in enumerate(s):
            if x == '(':
                stk.append(i)
            if x == ')':
                if len(stk) > 0 and s[stk[-1]] == '(':
                    stk.pop()
                else:
                    stk.append(i)
        print(stk)
        res = ''
        for i, x in enumerate(s):
            if len(stk) > 0 and i == stk[-1]:
                stk.pop()
            else:
                res += x
        return res

    def minRemoveToMakeValid2(self, s: str) -> str:
        if len(s) == 0:
            return s
        if len(s) == 1:
            if s[0] not in ['(',')']:
                return s
            else:
                return ""

        left, right = 0, len(s)-1
        left_cnt, right_cnt = 0, 0
        while left < right:
            if s[left] == '(':
                left_cnt += 1
            if s[right] == ')':
                right_cnt += 1
            left += 1
            right -= 1

        res = ""
        if left_cnt > right_cnt:
            tag = '('
            diff = left_cnt - right_cnt
        elif left_cnt < right_cnt:
            tag = ')'
            diff = right_cnt - left_cnt
        else:
            return s

        for x in s:
            if x == tag and diff > 0:
                diff -= 1
                continue
            else:
                res += x
        return res


if __name__ == '__main__':
    input = "())()((("
    sol = Solution()
    print(sol.minRemoveToMakeValid(input))