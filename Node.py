class Node:
    
    __slots__ = ['item', 'next']

    def __init__(self, item=None, next=None):
        self.item = item
        self.next = next