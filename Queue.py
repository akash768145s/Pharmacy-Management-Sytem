from Node import Node

class LinkedQueue:
    
    __slots__ = ['front', 'rear', 'size']
    
    def __init__(self):
        self.front = self.rear = Node()
        self.size = 0

    def __len__(self):
        return self.size

    def isempty(self):
        return self.front.next is None

    def enqueue(self, ele):
        self.rear.next = Node(ele)
        self.rear = self.rear.next
        self.size += 1

    def dequeue(self):
        if self.isempty():
            pass
        ele = self.front.next.item
        self.front = self.front.next
        self.size -= 1
        return ele
    
    def last_element(self):
        return self.rear.item

    def __iter__(self):
        current = self.front.next
        while current is not None:
            yield current.item
            current = current.next
