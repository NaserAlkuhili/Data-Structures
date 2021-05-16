# Overview
# In this notebook you will complete the following implementation of the balanced (AVL) binary search tree. 
# Note that you should not be implementing the map-based API described in the plain (unbalanced) BSTree notebook
#  — i.e., nodes in the AVLTree will only contain a single value.

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1 + AVLTree.Node.height(n.left), 1 + AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    
    @staticmethod
    def rebalance(node):
        if AVLTree.Node.height(node.left) > AVLTree.Node.height(node.right):
            if AVLTree.Node.height(node.left.left) >= AVLTree.Node.height(node.left.right):
                # left-left
                #print('left-left imbalance detected')
                node.rotate_right()
            else:
                # left-right
                #print('left-right imbalance detected')
                node.left.rotate_left()
                node.rotate_right()
        else:
            # right branch imbalance tests needed
            if AVLTree.Node.height(node.right.right) >= AVLTree.Node.height(node.right.left):
                #right-right 
                node.rotate_left()
            else:
                #right-left
                node.right.rotate_right()
                node.rotate_left()

    def add(self, val):  # O(log N)
        assert (val not in self)

        def add_rec(node):
            if not node:
                return AVLTree.Node(val)
            elif val < node.val:
                node.left = add_rec(node.left)
            else:
                node.right = add_rec(node.right)

            # detect and fix imbalance
            if abs(AVLTree.Node.height(node.left) - AVLTree.Node.height(node.right)) >= 2:
                AVLTree.rebalance(node)

            return node

        self.root = add_rec(self.root)
        self.size += 1

    def __delitem__(self, val):  # O(log N)
        assert (val in self)

        def delitem_rec(node):
            if val < node.val:
                node.left = delitem_rec(node.left)
            elif val > node.val:
                node.right = delitem_rec(node.right)
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    to_del = node.left
                    if not to_del.right:
                        node.left = to_del.left
                    else:
                        par = to_del
                        to_del = par.right
                        to_fix = [par]
                        while to_del.right:
                            par = par.right
                            to_fix.append(par)
                            to_del = to_del.right

                        # to_del refers to the right-most node, and par to its parent
                        par.right = to_del.left

                        # to_fix contains all the nodes I need to check for rebalancing
                        for n in to_fix[::-1]:  # traverse list in reverse
                            if abs(AVLTree.Node.height(n.left) - AVLTree.Node.height(n.right)) >= 2:
                                AVLTree.rebalance(n)

                    node.val = to_del.val

            # detect and fix imbalance (recursively)
            if abs(AVLTree.Node.height(node.left) - AVLTree.Node.height(node.right)) >= 2:
                AVLTree.rebalance(node)

            return node

        self.root = delitem_rec(self.root)
        self.size -= 1

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

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)

        yield from iter_rec(self.root)

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
                repr_str += '{val:^{width}}'.format(val=n.val, width=width // 2 ** level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""

        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1 + height_rec(t.left), 1 + height_rec(t.right))

        return height_rec(self.root)
