import collections

class Node:
    def __init__(self, left, right, val):
        self.left = left
        self.right = right
        self.val = val
        self.lchild = None
        self.rchild = None

def traverseBinaryTreeWidth(node, res, i = 0):
    
    if node.lchild:
        traverseBinaryTreeWidth(node.lchild, res, i+1)
    if node.rchild:
        traverseBinaryTreeWidth(node.rchild, res, i+1)



