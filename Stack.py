from Node import Node


class LinkedStack:

    def __init__(self):
        self.top = Node()
        self.size = 0

    def isempty(self):
        return self.top.next is None
    
    def __len__(self):
        return self.size
    
    def peek(self):
        if self.isempty():
            return
        return self.top.next.item
        
    def push(self, item):
        temp = Node(item, self.top.next)
        self.top.next = temp
        self.size += 1

    def pop(self):
        if self.isempty():
            return
        delnode = self.top.next
        self.top.next = delnode.next
        self.size -= 1
        return delnode.item
    
    def __str__(self):   
        pos = self.top.next
        result = '['
        while pos is not None:
            result += str(pos.item) + ','
            pos = pos.next
        return result[:-1] + ']'
    

    def __iter__(self):
        current = self.top.next
        while current is not None:
            yield current.item
            current = current.next

