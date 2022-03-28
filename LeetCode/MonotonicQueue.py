from typing import *
import collections

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        mq = collections.deque()
        mq.append(nums[0])
        res = []
        for i in range(1,k):
            self.monotonicQueuePush(mq, nums[i])
        res.append(mq[-1])
        for i in range(k, len(nums)):
            self.monotonicQueuePush(mq, nums[i])
            self.monotonicQueuePop(mq, nums[i-k])
            res.append(mq[-1])
        return res

    def monotonicQueuePop(self, q, val):
        if q[-1] == val:
            q.pop()
        return

    def monotonicQueuePush(self, q, val):
        while q and q[0] < val:
            q.popleft()
        q.appendleft(val)
        return

if __name__ == '__main__':
    input, k = [9,10,9,-7,-4,-8,2,-6], 5
    sol = Solution()
    res = sol.maxSlidingWindow(input, k)
    print(res)