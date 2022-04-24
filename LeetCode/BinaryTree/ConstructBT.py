from BinaryTreeUtils import *

class Solution:

    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not postorder:
            return None
        root = TreeNode(postorder[-1])
        pos = inorder.index(root.val)

        left_in = inorder[:pos]
        right_in = inorder[pos + 1:]

        # 1. Left nodes is always before the right nodes
        # 2. inorder and postorder are always the same length
        # 3. We don't need the last one in postorder as it is the root
        left_post = postorder[:len(left_in)]
        right_post = postorder[len(left_in):len(postorder) - 1]
        # left_post = [x for x in postorder if x in left_in]
        # right_post = [x for x in postorder if x in right_in]

        root.left = self.buildTree(left_in, left_post)
        root.right = self.buildTree(right_in, right_post)
        return root


if __name__ == '__main__':
    in_order = [9,3,15,20,7]
    post_order = [9,15,7,20,3]
    sol = Solution()
    root = sol.buildTree(in_order, post_order)
    res = []
    traverseBinaryTreeLevelOrder(root, res)
    print(res)