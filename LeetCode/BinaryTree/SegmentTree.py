from typing import *
import math
import collections
from BinaryTreeUtils import *


class NumArray:

    def __init__(self, nums: List[int]):
        left = 0
        right = len(nums)-1
        self.seg_tree = self.constructSegTree(left, right, nums)

    def constructSegTree(self, left, right, nums):
        node = Node(left, right, sum(nums[left:right+1]))
        if right > left:
            mid = math.floor((left + right) / 2)
            node.lchild = self.constructSegTree(left, mid, nums)
            node.rchild = self.constructSegTree(mid + 1, right, nums)
        return (node)

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        return (sum(self.nums[left:right + 1]))


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)

if __name__ == '__main__':
    node = NumArray([1, 2, 3, 4, 5]).seg_tree
    res = collections.deque()
    traverseBinaryTreeWidth(node, res)
    print(res)
