from BinaryTreeUtils import *


class Solution:

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        if not root:
            return root

        if root.val == key:
            return self.deleteNodeAtRoot(root)

        node = root
        while node:
            if node.left:
                if node.left.val == key:
                    node.left = self.deleteNodeAtRoot(node.left)
                    break
            if node.right:
                if node.right.val == key:
                    node.right = self.deleteNodeAtRoot(node.right)
                    break

            if node.val > key:
                node = node.left
            elif node.val < key:
                node = node.right

        return root

    def deleteNodeAtRoot(self, root):

        if not root:
            return None

        if not root.left or not root.right:
            return root.left if root.left else root.right
        else:
            left = root.left
            node = root.right
            while node.left:
                node = node.left
            node.left = left
            return root.right


if __name__ == '__main__':
    input = [5, 3, 6, 2, 4, None, 7]
    root = initBinaryTree(input)
    k = 3
    sol = Solution()
    res = sol.deleteNode(root, k)
    output = []
    traverseBinaryTreeLevelOrder(res, output)
    print(output)
