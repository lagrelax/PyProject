from utils import *


class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        res: str = "{Val: " + str(self.val)
        if self.left:
            res += '; Left: ' + str(self.left.val)
        else:
            res += '; Left: None'
        if self.right:
            res += '; Right: ' + str(self.right.val)
        else:
            res += '; Right: None'
        res += '}'
        return res

def initBinaryTree2(vals: List[int]) -> TreeNode:
    """ Pre-Order: Node, Left, Right"""
    nums = collections.deque(vals)
    tree = TreeNode(nums.popleft())
    nodes = collections.deque([tree])
    while nums:
        node = nodes[-1]
        if node and not node.val:
            nodes.pop()
            continue
        new_val = nums.popleft()
        new_node = TreeNode(new_val)
        if not node.left:
            node.left = new_node
            if new_node:
                nodes.appendleft(new_node)
            continue
        if not node.right:
            node.right = new_node
            if new_node:
                nodes.appendleft(new_node)
            nodes.pop()
    return tree


def initBinaryTree(vals: List[int], idx: int = 0) -> TreeNode:
    """
    Better way to init BT by only looking at the vals
    :param vals:
    :param idx:
    :return:
    """
    if idx >= len(vals):
        return None

    node = TreeNode(vals[idx])
    if 2 * idx + 1 < len(vals):
        node.left = initBinaryTree(vals, 2 * idx + 1)
    if 2 * idx + 2 < len(vals):
        node.right = initBinaryTree(vals, 2 * idx + 2)

    return node


def traverseBinaryTreePreOrder(root: TreeNode, res: List[int]) -> None:
    if root is None:
        return
    res.append(root.val)
    if root.left:
        traverseBinaryTreePreOrder(root.left, res)
    if root.right:
        traverseBinaryTreePreOrder(root.right, res)


def traverseBinaryTreeInOrder(root: TreeNode, res: List[int]) -> None:
    if root is None:
        return
    if root.left:
        traverseBinaryTreeInOrder(root.left, res)
    res.append(root.val)
    if root.right:
        traverseBinaryTreeInOrder(root.right, res)


def traverseBinaryTreePostOrder(root: TreeNode, res: List[int]) -> None:
    if root is None:
        return
    if root.left:
        traverseBinaryTreePostOrder(root.left, res)
    if root.right:
        traverseBinaryTreePostOrder(root.right, res)
    res.append(root.val)


def traverseBinaryTreePreOrderNoRecursive(root: TreeNode, res: List[int]) -> None:
    nodes = [root]
    while nodes:
        node = nodes.pop()
        res.append(node.val)
        if node.right:
            nodes.append(node.right)
        if node.left:
            nodes.append(node.left)


def traverseBinaryTreeLevelOrder(root: TreeNode, res: List[int]) -> None:
    nodes = collections.deque([root])
    while nodes:
        node = nodes.pop()
        res.append(node.val)
        if node.left:
            nodes.appendleft(node.left)
        if node.right:
            nodes.appendleft(node.right)


if __name__ == '__main__':
    bt = initBinaryTree([1, 2, 3, 4, 5, 6, 7])
    res = []
    traverseBinaryTreePreOrder(bt, res)
    print(res)
    res = []
    traverseBinaryTreeInOrder(bt, res)
    print(res)
    res = []
    traverseBinaryTreePostOrder(bt, res)
    print(res)
    res = []
    traverseBinaryTreeLevelOrder(bt, res)
    print(res)
