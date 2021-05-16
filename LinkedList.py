class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next  = next
    
    def __init__(self):
        self.head = LinkedList.Node(None) # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head # set up "circular" topology
        self.length = 0
        
        
    ### prepend and append, below, from class discussion
        
    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1
        
    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1
            
            
    ### subscript-based access ###

    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx

    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert (isinstance(idx, int))
        nindx = self._normalize_idx(idx)
        if nindx >= self.length:
            raise IndexError
        curr = self.head.next
        for i in range(self.length):
            if i == nindx:
                return curr.val
            curr = curr.next

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert (isinstance(idx, int))
        nindx = self._normalize_idx(idx)
        if nindx >= self.length:
            raise IndexError
        curr = self.head.next
        for i in range(self.length):
            if i == nindx:
                curr.val = value
            curr = curr.next


    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert (isinstance(idx, int))
        nindx = self._normalize_idx(idx)
        if nindx >= self.length:
            raise IndexError
        curr = self.head.next
        for i in range(self.length):
            if i == nindx:
                curr.prior.next = curr.next
                curr.next.prior = curr.prior
                self.length -=1
            curr = curr.next

    ### cursor-based access ###

    def cursor_get(self):
        """retrieves the value at the current cursor position"""
        assert self.cursor is not self.head
        return self.cursor.val

    def cursor_set(self, idx):
        """sets the cursor to the node at the provided index"""
        self.cursor = self.head.next
        self.cursor_indx = 0
        for i in range(idx):
            self.cursor = self.cursor.next
            self.cursor_indx += 1


    def cursor_move(self, offset):
        """moves the cursor forward or backward by the provided offset
        (a positive or negative integer); note that it is possible to advance
        the cursor by further than the length of the list, in which case the
        cursor will just "wrap around" the list, skipping over the sentinel
        node as needed"""
        assert len(self) > 0
        if offset > 0:
            while offset != 0:
                self.cursor = self.cursor.next
                if self.cursor_indx < self.length:
                    self.cursor_indx += 1
                else:
                    self.cursor_indx = 0
                offset -=1

        elif offset < 0:
            while offset != 0:
                self.cursor = self.cursor.prior
                if self.cursor_indx > 0:
                    self.cursor_indx -= 1
                else:
                    self.cursor_indx = self.length
                offset +=1






    def cursor_insert(self, value):
        """inserts a new value after the cursor and sets the cursor to the
        new node"""
        newNode = LinkedList.Node(value, self.cursor, self.cursor.next)
        self.cursor.next.prior = newNode
        self.cursor.next = newNode
        self.cursor = self.cursor.next
        self.cursor_indx +=1
        self.length += 1


    def cursor_delete(self):
        """deletes the node the cursor refers to and sets the cursor to the
        following node"""
        assert  self.cursor is not self.head and len(self) > 0
        tempIndx = self.cursor_indx
        self.cursor = self.cursor.next
        del self[tempIndx]
        

    ### stringification ###

    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        if self.length == 1:
            return "[" + str(self.head.next.val) + "]"
        elif self.length == 0:
            return "[]"

        else:
            strData = ""
            curr = self.head.next
            for i in range(self.length-1):
                strData += str(curr.val) + ", "
                curr = curr.next

            strData += str(self.__getitem__(self.length-1))
            finalStr = "[" + strData + "]"
            return finalStr


    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        return self.__str__()
            


    ### single-element manipulation ###

    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""

        nindx = self._normalize_idx(idx)
        curr = self.head.next

        if nindx > self.length:
            raise IndexError
        elif nindx == self.length:
            self.append(value)
        else:

            for i in range(nindx):
                curr = curr.next

        newNode = LinkedList.Node(value, curr.prior, curr)
        curr.prior.next = newNode
        curr.prior = newNode
        self.length +=1



    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""

        nindx = self._normalize_idx(idx)
        val = self[nindx]
        del self[nindx]
        return val

    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        found = False
        curr = self.head.next
        index = 0
        for i in range(self.length):
            if curr.val == value:
                index = i
                found = True
                break
            curr = curr.next
        if found:
            del self[index]
        else:
            raise ValueError
        
    

    ### predicates (T/F queries) ###

    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        equal = True
        if self.length != other.length:
            equal = False
        for i in range(self.length):
            if self[i] != other[i]:
                equal = False
        return equal
                

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        contains = False
        for i in range(self.length):
            if self[i] == value:
                contains = True
        return contains
        


    ### queries ###

    def __len__(self):
        """Implements `len(self)`"""
        return self.length

    def min(self):
        """Returns the minimum value in this list."""
        curr = self.head.next
        min = curr.val
        for i in range(self.length):
            if min > curr.val:
                min = curr.val
            curr = curr.next
        return min

    def max(self):
        """Returns the maximum value in this list."""
        curr = self.head.next
        max = curr.val
        for i in range(self.length):
            if max < curr.val:
                max = curr.val
            curr = curr.next
        return max

    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        found = False
        newI = self._normalize_idx(i)

        if j == None and not found:
            for i in range(newI,self.length):
                if self[i] == value:
                    found = True
                    return i

        elif j != None and not found:
            newJ = self._normalize_idx(j)
            for i in range(newI,newJ):
                if self[i] == value:
                    found = True
                    return i


        if not found:
            raise ValueError



    def count(self, value):
        """Returns the number of times value appears in this list."""
        counter = 0
        curr = self.head.next
        for i in range(self.length):
            if curr.val == value:
                counter += 1
            curr = curr.next
        return counter
        

    
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those
        of other."""
        assert (isinstance(other, LinkedList))

        newLinkedList = LinkedList()
        
        if self.length > 0:
            for value in self:
                newLinkedList.append(value)
                
        if other.length > 0:
            for value in other:
                newLinkedList.append(value)

        return newLinkedList




    def clear(self):
        """Removes all elements from this list."""
        self.head.prior = self.head.next = self.head
        self.length = 0

    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""

        newLinkedList = LinkedList()

        for value in self:
            newLinkedList.append(value)

        return newLinkedList

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for value in other:
            self.append(value)

        return self
        

            
    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        curr = self.head.next
        while curr and curr.val != None:
            yield curr.val
            curr = curr.next
