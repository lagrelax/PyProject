from BinaryTreeUtils import *


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        stk = collections.deque([])
        if root.left:
            stk.appendleft(root.left)

        if root.right:
            stk.appendleft(root.right)

        res = root

        while stk:
            node = stk.pop()
            if min(p.val, q.val) <= node.val <= max(p.val, q.val):
                res = node
                if node.left:
                    stk.appendleft(node.left)
                if node.right:
                    stk.appendleft(node.right)
            else:
                return res

if __name__ == '__main__':
    input = [6,2,8,0,4,7,9,None,None,3,5]
    p, q = 2, 8
    sol = Solution()
    root = initBinaryTree(input)
    res = sol.lowestCommonAncestor(root,TreeNode(p),TreeNode(q))
    print(res.val)
