# 1. Augmenting the Heap with a key function
# The heap implementation covered in class is for a so-called "max-heap" — i.e., one where elements are organized 
# such that the one with the maximum value can be efficiently extracted.

# This limits our usage of the data structure, however. Our heap can currently only accommodate elements that have 
# a natural ordering (i.e., they can be compared using the '>' and '<' operators as used in the implementation), 
# and there's no way to order elements based on some partial or computed property.

# To make our heap more flexible, you'll update it to allow a key function to be passed to its initializer. 
# This function will be used to extract a value from each element added to the heap; these values, in turn, 
# will be used to order the elements.

# We can now easily create heaps with different semantics, e.g.,

# Heap(len) will prioritize elements based on their length (e.g., applicable to strings, sequences, etc.)
# Heap(lambda x: -x) can function as a min-heap for numbers
# Heap(lambda x: x.prop) will prioritize elements based on their prop attribute
# If no key function is provided, the default max-heap behavior should be used — 
# the "lambda x:x" default value for the __init__ method does just that.

# You will, at the very least, need to update the _heapify and add methods, below, to complete this assignment. 
# (Note, also, that pop_max has been renamed pop, while max has been renamed peek, to reflect their more general nature.)

class Heap:
    def __init__(self, key=lambda x: x):
        self.data = []
        self.key = key

    @staticmethod
    def _parent(idx):
        return (idx - 1) // 2

    @staticmethod
    def _left(idx):
        return idx * 2 + 1

    @staticmethod
    def _right(idx):
        return idx * 2 + 2

    def _compare(self, p1, p2):
        if self.key(self.data[p1]) > self.key(self.data[p2]):
            return p1

        else:
            return p2

    def heapify(self, idx=0):
        Lr = self._left(idx)
        Rr = self._right(idx)
        maxIdx = idx

        if Lr < len(self.data) and self.key(self.data[Lr]) > self.key(self.data[maxIdx]):
            maxIdx = Lr
        if Rr < len(self.data) and self.key(self.data[Rr]) > self.key(self.data[maxIdx]):
            maxIdx = Rr

        if maxIdx != idx:
            self.data[maxIdx], self.data[idx] = self.data[idx], self.data[maxIdx]
            self.heapify(maxIdx)





    def add(self, x):
        self.data.append(x)
        length = len(self) - 1
        parent = self._parent(length)

        while length > 0 and self.key(self.data[parent]) < self.key(self.data[length]):
            self.data[length], self.data[parent] = self.data[parent], self.data[length]
            length = parent
            parent = self._parent(parent)


    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data) - 1]
        del self.data[len(self.data) - 1]
        self.heapify()
        return ret

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)




### Excercise ###

def running_medians(iterable):
    minHeap = Heap(key=lambda x: -x)
    maxHeap = Heap()
    medians = []
    currMedian = 0
    for i , x in enumerate(iterable):
        if x >= currMedian:
            minHeap.add(x)
        elif x <= currMedian:
            maxHeap.add(x)

        #Making sure both the length difference
        #between the two heaps does not exceed 1
        if len(minHeap) - len(maxHeap) > 1:
            maxHeap.add(minHeap.pop())
        elif len(maxHeap) - len(minHeap) > 1:
            minHeap.add(maxHeap.pop())
            
        if len(maxHeap) == len(minHeap):
            currMedian = (maxHeap.peek() + minHeap.peek()) / 2
        
        elif len(maxHeap) > len(minHeap):
            currMedian = maxHeap.peek()
        elif len(maxHeap) < len(minHeap):
            currMedian = minHeap.peek()
            
        medians.append(currMedian)
    
    return medians


