from utils import *

class Solution:
    def calculate(self, s: str) -> int:

        operators = ['+', '-', '*', '/']
        stk = []
        tmp = ''
        tag = None
        for x in s:
            if x not in operators:
                tmp += x
            else:
                num = int(tmp)
                if tag is not None:
                    self.do_operation(num, stk, tag)
                else:
                    stk.append(num)
                tag = x
                tmp = ''

        num = int(tmp)
        if tag is not None:
            self.do_operation(num, stk, tag)
        else:
            stk.append(num)

        return sum(stk)

    def do_operation(self, num, stk, tag):
        if tag == '+':
            stk.append(num)
        elif tag == '-':
            stk.append(-num)
        elif tag == '*':
            prev = stk.pop()
            stk.append(prev * num)
        else:
            prev = stk.pop()
            sign = prev/abs(prev) if prev != 0 else 1
            stk.append(int(sign * (abs(prev) // num)))


if __name__ == '__main__':
    input = "0/1"
    sol = Solution()
    s = sol.calculate(input)
    print(s)