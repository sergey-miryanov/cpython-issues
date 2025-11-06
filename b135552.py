class BaseNode:
    def __del__(self):
        BaseNode.next = BaseNode.next.next

class Node(BaseNode):
    pass

BaseNode.next = Node()
BaseNode.next.next = Node()

import gc
gc.collect(2)

