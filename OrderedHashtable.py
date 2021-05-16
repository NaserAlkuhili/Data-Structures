class OrderedHashtable:
    class Node:
        """This class is used to create nodes in the singly linked "chains" in
        each hashtable bucket."""

        def __init__(self, index, next=None):
            # don't rename the following attributes!
            self.index = index
            self.next = next

    def __init__(self, n_buckets=1000):
        # the following two variables should be used to implement the "two-tiered"
        # ordered hashtable described in class -- don't rename them!
        self.indices = [None] * n_buckets
        self.entries = []
        self.count = 0

    def __getitem__(self, key):
        indx = hash(key) % len(self.indices)
        curr = self.indices[indx]
        while curr:
            index = curr.index
            if self.entries[index] != None:
                if self.entries[index][0] == key:
                    return self.entries[curr.index][1]
            curr = curr.next

        raise KeyError

    def __setitem__(self, key, val):
        bucket_idx = hash(key) % len(self.indices)
        b = self.indices[bucket_idx]
        while b:
            if (not self.entries[b.index] == None) and (self.entries[b.index][0] == key):
                self.entries[b.index][1] = val
                return
            b = b.next

        else:
            self.entries.append([key,val])
            self.indices[bucket_idx] = OrderedHashtable.Node(len(self.entries) - 1, next=self.indices[bucket_idx])
            self.count += 1


    def __delitem__(self, key):
        bucket_idx = hash(key) % len(self.indices)
        b = self.indices[bucket_idx]
        while b:
            idx = b.index
            if self.entries[idx] != None:
                if (self.entries[idx][0] == key):
                    self.entries[idx] = None
                    self.count -= 1
                    return
            b = b.next
        else:
            raise KeyError

    # Implement the contains method

    def __contains__(self, key):

        try:

            _ = self[key]

            return True

        except:

            return False

    # implement length of the dictionary method

    def __len__(self):

        return self.count

    def __iter__(self):

        for i in range(len(self.entries)):
            if self.entries[i] != None:
                yield self.entries[i][0]



    # implement the Keys method

    def keys(self):

        return iter(self)

    def values(self):

        for i in range(len(self.entries)):
            if self.entries[i] != None:
                yield self.entries[i][1]

    def items(self):

        for i in range(len(self.entries)):
            if self.entries[i] != None:
                yield self.entries[i]

    def __str__(self):

        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'

    def __repr__(self):

        return str(self)
