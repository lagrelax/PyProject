from BinaryTreeUtils import *


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        node = root
        while True:
            print(node.val)
            if node.val < min(p.val, q.val):
                node = node.right
            elif node.val > max(p.val, q.val):
                node = node.left
            else:
                return node

if __name__ == '__main__':
    input = [6,2,8,0,4,7,9,None,None,3,5]
    p, q = 2, 8
    sol = Solution()
    root = initBinaryTree(input)
    res = sol.lowestCommonAncestor(root,TreeNode(p),TreeNode(q))
    print(res.val)
