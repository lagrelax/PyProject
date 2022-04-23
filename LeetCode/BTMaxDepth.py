from typing import *
from BinaryTreeUtils import *
import collections


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        res = 0
        q = collections.deque([root])
        while q:
            res += 1
            for _ in range(len(q)):
                node = q.pop()
                if not node.left:
                    q.appendleft(node.left)
                if not node.right:
                    q.appendleft(node.right)
        return res

if __name__ == '__main__':
    input = [3,9,20,None ,None ,15,7]
    root = initBinaryTree(input)
    sol = Solution()
    print(sol.maxDepth(root))