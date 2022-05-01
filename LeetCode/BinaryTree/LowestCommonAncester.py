from BinaryTreeUtils import *


class Solution:

    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        stk = collections.deque()
        if root.right:
            stk.append(root.right)
        if root.left:
            stk.append(root.left)

        res = root
        while stk:
            node = stk.pop()
            if self.isDescendant(node, p.val) and self.isDescendant(node, q.val):
                res = node
                if node.right:
                    stk.append(node.right)
                if node.left:
                    stk.append(node.left)
        return res

    def isDescendant(self, node, target):

        if not node:
            return False

        if node.val == target:
            return True

        if not node.left and not node.right:
            return node.val == target

        left = self.isDescendant(node.left, target) if node.left else False
        right = self.isDescendant(node.right, target) if node.left else False
        return left or right


if __name__ == '__main__':
    input = [9,-1,-4,10,3,None,None,None,5]
    p, q = TreeNode(3), TreeNode(5)
    root = initBinaryTree(input)
    sol = Solution()
    r = sol.lowestCommonAncestor(root, p, q)
    print(r.val)
