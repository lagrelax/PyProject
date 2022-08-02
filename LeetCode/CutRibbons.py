from utils import *


class Solution:
    def maxLength(self, ribbons: List[int], k: int) -> int:
        l, r = 1, max(ribbons)
        if k > r:
            return 0

        prev = (l + r) // 2
        while l <= r:
            mid = (l + r) // 2
            res = 0
            for r in ribbons:
                res += r // mid
            # less res, mid too long, make shorter
            if res < k:
                r = mid - 1
            else:
                prev = mid
                l = mid + 1
        return prev


if __name__ == '__main__':
    inputs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 100000, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    k = 49
    sol = Solution()
    print(sol.maxLength(inputs, k))
