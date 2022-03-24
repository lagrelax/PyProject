
class ListNode:
    def __init__(self,val = 0, next = None):
        self.val = val
        self.next = next

def printListNode(node: ListNode):
    i = 0
    current = node
    res = []
    while current:
        res.append(current.val)
        current = current.next
    print(res)

def initListNode(input):
    inputNS = None

    for x in input:
        node = ListNode(val=x)
        if inputNS is None:
            inputNS = node
            current = inputNS
        else:
            current.next = node
            current = current.next

    return(inputNS)