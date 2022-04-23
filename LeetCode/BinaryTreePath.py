from BinaryTreeUtils import *


class Solution:

    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        q = collections.deque([root])
        res = []
        path = collections.deque([str(root.val)])
        while q:
            for _ in range(len(q)):
                node = q.pop()
                st = path.pop()
                if node.right:
                    path.append(st+'->'+str(node.right.val))
                    q.append(node.right)
                if node.left:
                    path.append(st+'->'+str(node.left.val))
                    q.append(node.left)
                if node.val and not node.left and not node.right:
                    res.append(st)
        return res


if __name__ == '__main__':
    input = [1, 2, 3, None, 5]
    root = initBinaryTree(input)
    root2 = initBinaryTree2(input)
    sol = Solution()
    res = sol.binaryTreePaths(root)
