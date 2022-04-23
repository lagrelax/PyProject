from typing import *
import collections
from BinaryTreeUtils import *

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
        if root.left is None and root.right is None:
            return True

        q = collections.deque([(root.left, root.right)])
        while q:
            pair = q.pop()
            if pair[1] is None and pair[0] is None:
                continue
            elif pair[0] is None or pair[1] is None:
                return False

            if pair[0].val != pair[1].val:
                return False
            else:
                out_pair = (pair[0].left, pair[1].right)
                in_pair = (pair[0].right, pair[1].left)
                q.appendleft(out_pair)
                q.appendleft(in_pair)

        return True

    def isSymmetricRecursive(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
        if root.left is None and root.right is None:
            return True
        return self.isMirror(root.left, root.right)

    def isMirror(self, left, right):
        if left is None and right is None:
            return True
        elif left is None or right is None:
            return False

        if left.val == right.val:
            out_pair = self.isMirror(left.left, right.right)
            in_pair = self.isMirror(left.right, right.left)
            return out_pair and in_pair
        else:
            return False

if __name__ == '__main__':
    sol = Solution()
    input = [2,3,3,4,5,5]
    root = initBinaryTree(input)
    print(sol.isSymmetric(root))