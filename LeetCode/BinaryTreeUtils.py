from typing import *
import collections

class BTreeNode:
    def __init__(self, val = 0):
        self.val = val
        self.lchild = None
        self.rchild = None

def initBinaryTree(vals: List[int]) -> BTreeNode:
    """ Order: Node, Left, Right"""
    nums = collections.deque(vals)
    tree = BTreeNode(nums.popleft())
    nodes = collections.deque([tree])
    while nums:
        node = nodes[-1]
        new_node = BTreeNode(nums.popleft())
        if not node.lchild:
            node.lchild = new_node
            nodes.appendleft(new_node)
            continue
        if not node.rchild:
            node.rchild = new_node
            nodes.appendleft(new_node)
            nodes.pop()
    return tree


def traverseBinaryTreePreOrder(root: BTreeNode, res: List[int]) -> None:
    if root is None:
        return
    res.append(root.val)
    if root.lchild:
        traverseBinaryTreePreOrder(root.lchild, res)
    if root.rchild:
        traverseBinaryTreePreOrder(root.rchild, res)

def traverseBinaryTreeInOrder(root: BTreeNode, res: List[int]) -> None:
    if root is None:
        return
    if root.lchild:
        traverseBinaryTreeInOrder(root.lchild, res)
    res.append(root.val)
    if root.rchild:
        traverseBinaryTreeInOrder(root.rchild, res)

def traverseBinaryTreePostOrder(root: BTreeNode, res: List[int]) -> None:
    if root is None:
        return
    if root.lchild:
        traverseBinaryTreePostOrder(root.lchild, res)
    if root.rchild:
        traverseBinaryTreePostOrder(root.rchild, res)
    res.append(root.val)

def traverseBinaryTreePreOrderNoRecursive(root: BTreeNode, res: List[int]) -> None:
    nodes = [root]
    while nodes:
        node = nodes.pop()
        res.append(node.val)
        if node.rchild:
            nodes.append(node.rchild)
        if node.lchild:
            nodes.append(node.lchild)

def traverseBinaryTreeLevelOrder(root: BTreeNode, res: List[int]) -> None:
    nodes = collections.deque([root])
    while nodes:
        node = nodes.pop()
        res.append(node.val)
        if node.lchild:
            nodes.appendleft(node.lchild)
        if node.rchild:
            nodes.appendleft(node.rchild)

if __name__ == '__main__':
    bt = initBinaryTree([1,2,3,4,5,6,7])
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