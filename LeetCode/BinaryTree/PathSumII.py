from BinaryTreeUtils import *


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res = []
        stk = [[root.val]]
        q = collections.deque([root])

        while q:
            node = q.pop()
            s = stk.pop()
            print(s)
            if not node.left and not node.right and sum(s) == targetSum:
                res.append(s)

            if node.right:
                q.append(node.right)
                s.append(node.right.val)
                stk.append(s)
            if node.left:
                q.append(node.left)
                s.append(node.left.val)
                stk.append(s)

        return res

if __name__ == '__main__':
    input = [5,4,8,11,None,13,4,7,2,None,None,5,1]
    t = 22
    root = initBinaryTree(input)
    sol = Solution()
    print(sol.pathSum(root,sol))
