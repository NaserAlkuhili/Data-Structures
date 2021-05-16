# Exercise 1: BSTree operations
# For this exercise you'll implement three additional methods in the binary search tree data structure completed
# in class, so that you have an opportunity to practice both using the recursive pattern covered in class and 
# navigating the binary tree structure.

# The methods you'll implement are:

# count_less_than: takes an argument x, and returns the number of elements in the tree with values less than x
# successor: takes an argument x, and returns the smallest value from the tree that is larger than x 
# (note that x itself does not need to be in the tree); if there are no values larger than x, returns None
# descendants: takes an argument x, and returns all descendants of x in the tree (i.e., all values in the subtree rooted at x),
# ordered by value; if x has no descendants or does not exist in the tree, returns an empty list
# The cell below contains the (read-only) BSTree implementation from lecture. Beneath that is the cell containing the methods you will be implementing, followed by unit test cells.

class BSTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
            
    def __init__(self):
        self.size = 0
        self.root = None

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def add(self, val):
        assert(val not in self)
        def add_rec(node):
            if not node:
                return BSTree.Node(val)
            elif val < node.val:
                return BSTree.Node(node.val, left=add_rec(node.left), right=node.right)
            else:
                return BSTree.Node(node.val, left=node.left, right=add_rec(node.right))
        self.root = add_rec(self.root)
        self.size += 1
        
    def __delitem__(self, val):
        assert(val in self)
        def delitem_rec(node):
            if val < node.val:
                node.left = delitem_rec(node.left)
                return node
            elif val > node.val:
                node.right = delitem_rec(node.right)
                return node
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    # remove the largest value from the left subtree as a replacement
                    # for the root value of this tree
                    t = node.left # refers to the candidate for removal
                    if not t.right:
                        node.val = t.val
                        node.left = t.left
                    else:
                        n = t
                        while n.right.right:
                            n = n.right
                        t = n.right
                        n.right = t.left
                        node.val = t.val
                    return node
                
        self.root = delitem_rec(self.root)
        self.size -= 1

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
                    
        return iter_rec(self.root)
            
    def __len__(self):
        return self.size
    
    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)
    
    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)
class BSTree(BSTree):
    def count_less_than(self, x):
        def count_rec(node, n):
            if not node:
                return 0
            else:
                if n > node.val:
                    return 1 + count_rec(node.left, n) + count_rec(node.right, n)
                else:
                    return count_rec(node.left, n)
        return count_rec(self.root, x)




    def successor(self, x):
        def succ_rec(node, s):
            if not node:
                return None
            elif node.val <= s:
                return succ_rec(node.right, s)
            else:
                if succ_rec(node.left, s) is None:
                    return node.val
                else:
                    return succ_rec(node.left, s)
        return succ_rec(self.root, x)

    def descendants(self, x):
        if x in self:
            def right_rec(node):
                lst = []
                newList = []
                while node:
                    lst.append(node.val)
                    newList += right_rec(node.left)
                    node = node.right
                return lst + newList

            def left_rec(node):
                lst = []
                newList = []
                while node:
                    lst.append(node.val)
                    newList += left_rec(node.right)
                    node = node.left
                return lst + newList

            def desc_rec(node, n):
                if not node:
                    return None
                elif node.val > n:
                    return desc_rec(node.left, n)
                elif node.val < n:
                    return desc_rec(node.right, n)
                else:
                    descList = left_rec(node.left) + right_rec(node.right)
                    return descList
            return sorted(desc_rec(self.root, x))
        else:
            return []



# Exercise 2: BSTree as a mapping structure
# For this next exercise you will re-implemet the binary search tree so that it can be used as a mapping structure. 
# The Node class will be updated so as to hold separate key and value attributes 
# (instead of a single value, as it currently does), and instead of the add method, 
# you should implement the __getitem__ and __setitem__ methods in order to associate keys and values.
# __delitem__, __contains__, and __iter__ will also need to be updated, to perform key-based removal, search,
# and iteration. Finally, the keys, values, and items methods will return iterators that allow the keys, values, 
# and key/value tuples of the tree (all sorted in order of their associated keys) to be traversed.

# If __setitem__ is called with an existing key, the method will simply locate the associated node and update its value with 
# the newly provided value (as you would expect a mapping structure to do). If either __getitem__ or __delitem__ are called 
# with a key that does not exist in the tree, a KeyError should be raised.

# The API described above will allow the tree to be used as follows:

# t = BSTree()
# t[0] = 'zero'
# t[5] = 'five'
# t[2] = 'two'

# print(t[5])

# t[5] = 'FIVE!!!'

# for k,v in t.items():
#     print(k, '=', v)

# del t[2]

# print('length =', len(t))

# The expected output of the above follows:

# five
# 0 = zero
# 2 = two
# 5 = FIVE!!!
# length = 2

# The following BSTree class contains an updated Node, and stubs for the methods you are to implement. 
# The first few simple test cases beneath the class definition should help clarify the required behavior.

class BSTree:
    class Node:
        def __init__(self, key, val, left=None, right=None):
            self.key = key
            self.val = val
            self.left = left
            self.right = right

    def __init__(self):
        self.size = 0
        self.root = None

    def __getitem__(self, key):
        def get_rec(node):
            if not node:
                raise KeyError
            elif key < node.key:
                return get_rec(node.left)
            elif key > node.key:
                return get_rec(node.right)
            elif key == node.key:
                return node.val
            else:
                raise KeyError

        return get_rec(self.root)



    def __setitem__(self, key, val):
        def rec_setItem(node):
            if not node:
                return BSTree.Node(key,val)
            elif node.key < key:
                node.right = rec_setItem(node.right)
                return node
            elif node.key > key:
                node.left = rec_setItem(node.left)
                return node
            else:
                node.val = val
                return node

        self.root = rec_setItem(self.root)
        self.size += 1

    def __delitem__(self, key):
        def delitem_rec(node):
            if key < node.key:
                node.left = delitem_rec(node.left)
                return node
            elif key > node.key:
                node.right = delitem_rec(node.right)
                return node
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    t = node.left
                    if not t.right:
                        node.key = t.key
                        node.left = t.left
                    else:
                        n = t
                        while n.right.right:
                            n = n.right
                        t = n.right
                        n.right = t.left
                        node.key = t.key
                    return node
        self.root = delitem_rec(self.root)
        self.size -= 1

    def __contains__(self, key):
        def find(node):
            if not node:
                return False
            elif key > node.key:
                return find(node.right)
            elif key < node.key:
                return find(node.left)
            elif key == node.key:
                return True

        return find(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def rec_iter(node):
            if node:
                yield node
                yield from rec_iter(node.right)
                yield from rec_iter(node.left)
        yield from rec_iter(self.root)

    def keys(self):
        def rec_keys(node):
            if node:
                yield node.key
                yield from rec_keys(node.left)
                yield from rec_keys(node.right)
        return sorted(rec_keys(self.root))





    def values(self):
        for k in self.keys():
            yield self[k]

    def items(self):
        for k in self.keys():
            yield k, self[k]

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n, level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height - 1:
                    nodes.extend([(None, level + 1), (None, level + 1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width // 2 ** level)
            elif n:
                if n.left or level < height - 1:
                    nodes.append((n.left, level + 1))
                if n.right or level < height - 1:
                    nodes.append((n.right, level + 1))
                repr_str += '{val:^{width}}'.format(val=n.key, width=width // 2 ** level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""

        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1 + height_rec(t.left), 1 + height_rec(t.right))

        return height_rec(self.root)
