from BinaryTreeUtils import *


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        res = 0
        path_stk = collections.deque()
        q = collections.deque([root])

        while q:
            for _ in range(len(q)):
                if len(path_stk) == 0:
                    path = []
                else:
                    path = path_stk.pop()
                node = q.pop()
                path.append(node.val)
                if node.left and node.left.val:
                    q.appendleft(node.left)
                    path_stk.appendleft(path[:])
                if node.right and node.right.val:
                    q.appendleft(node.right)
                    path_stk.appendleft(path[:])
                if not node.left and not node.right:
                    tmp = 0
                    for i, x in enumerate(path):
                        tmp += x * 10**(len(path)-1-i)
                    res += tmp
        return res



if __name__ == '__main__':
    inputs = [1, 2, 3]
    inputs = [6,4,1,6,None,None,None,None,4,2,None,6]
    root = initBinaryTree2(inputs)
    sol = Solution()
    res = sol.sumNumbers(root)
    print(res)
