class Stack:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next  = next
    
    def __init__(self):
        self.top = None

    def push(self, val):
        self.top = Stack.Node(val, self.top)
        
    def pop(self):
        assert self.top, 'Stack is empty'
        val = self.top.val
        self.top = self.top.next
        return val
    
    def peek(self):
        return self.top.val if self.top else None
    
    def empty(self):
        return self.top == None
    
    def __bool__(self):
        return not self.empty()
    
    def __repr__(self):
        if not self.top:
            return ''
        return '--> ' + ', '.join(str(x) for x in self)
    
    def __iter__(self):
        n = self.top
        while n:
            yield n.val
            n = n.next


### Stacks Excercises ###

# 1. Paired delimiter matching
# In class we wrote a function that uses a stack to help determine whether all
# paired delimiters (e.g., parentheses) in a given string are correctly matched
# — you can review the code at http://moss.cs.iit.edu/cs331/notebooks/stacks-and-queues.html (look for check_parens).

# For this first exercise you will extend our implementation to check all the following
# paired delimiters: {}, (), [], <>. We've defined two strings — delim_openers and delim_closers
# — that might come in handy in your implementation (hint: look into using the index sequence method).

delim_openers = '{([<'
delim_closers = '})]>'

def check_delimiters(expr):
    """Returns True if and only if `expr` contains only correctly matched delimiters, else returns False."""
    s = Stack()
    newExpr = expr.replace(" ", "")
    if len(newExpr) ==1:
        return False
    else:
        for c in newExpr:
            if c in delim_openers:
                s.push(c)
            elif c in delim_closers:
                toCheck = delim_openers[delim_closers.index(c)]
                if toCheck in s and s.empty() == False:
                        s.pop()
                else:
                    return False
    return s.empty()



# 2. Infix → Postfix conversion
# Another function we looked at was one that used a stack to evaluate a postfix arithmetic expression — you can review the 
# code at http://moss.cs.iit.edu/cs331/notebooks/stacks-and-queues.html (look for eval_postfix). Because most of us are more
#  accustomed to infix-form arithmetic expressions (e.g., 2 * (3 + 4)), however, the function seems to be of limited use. 
# The good news: we can use a stack to convert an infix expression to postfix form!

# To do so, we will use the following algorithm:

# Start with an empty list and an empty stack. At the end of the algorithm, the list will contain the correctly ordered tokens of the postfix expression.

# Next, for each token in the expression (split on whitespace):

# if the token is a digit (the string isdigit method can be used to determine this), simply append it to the list; else, the token must be either an operator or an opening or closing parenthesis, in which case apply one of the following options:

# if the stack is empty or contains a left parenthesis on top, push the token onto the stack.

# if the token is a left parenthesis, push it on the stack.

# if the token is a right parenthesis, pop the stack and append all operators to the list until a left parenthesis is popped. Discard the pair of parentheses.

# if the token has higher precedence than the top of the stack, push it on the stack. For our purposes, the only operators are +, -, *, /, where the latter two have higher precedecence than the first two.

# if the token has equal precedence with the top of the stack, pop and append the top of the stack to the list and then push the incoming operator.

# if the incoming symbol has lower precedence than the symbol on the top of the stack, pop the stack and append it to the list. Then repeat the above tests against the new top of stack.

# After arriving at the end of the expression, pop and append all operators on the stack to the list.

# A writeup containing a detailed explanation of the steps above (though it prints the tokens immediately rather than adding them to a list) can be found at http://csis.pace.edu/~wolf/CS122/infix-postfix.htm

# you may find the following precedence dictionary useful
prec = {'*': 2, '/': 2,
        '+': 1, '-': 1}

def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    ops = Stack()
    postfix = []
    toks = expr.split()
    def tests(chr):
        if chr.isdigit():
            postfix.append(chr)

        elif chr == '(':
            ops.push('(')

        elif ops.peek() == '(' or ops.empty():
            ops.push(chr)

        elif chr ==')':
            while ops.peek() != "(":
                postfix.append(ops.pop())
            ops.pop()

        elif chr in prec and prec[chr] > prec[ops.peek()]:
            ops.push(chr)

        elif chr in prec and prec[chr] == prec[ops.peek()]:
            postfix.append(ops.pop())
            ops.push(chr)

        elif chr in prec and prec[chr] < prec[ops.peek()]:
            postfix.append(ops.pop())
            tests(chr)

    for tok in toks:
        tests(tok)


    while not ops.empty():
        postfix.append(ops.pop())


    return ' '.join(postfix)




### Queues ###

class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    def enqueue(self, val):
        if self.head == 0 and self.tail == len(self.data) -1:
            raise RuntimeError
        if self.head - self.tail == 1:
            raise RuntimeError


        elif self.head == -1 and self.tail == -1:
            self.data[0] = val
            self.head += 1
            self.tail += 1
        else:
            if len(self.data)- 1 == self.tail and self.head != 0:
                self.tail = -1
            self.data[self.tail+1] = val
            self.tail += 1


    def dequeue(self):
        if self.empty() == False:

            if self.head == self.tail:
                toReturn = self.data[self.head]
                self.data[self.head] = None
                self.head = -1
                self.tail = -1
                return toReturn

            index = self.head
            toReturn = self.data[index]
            self.data[index] = None
            if index+1 < len(self.data):
                self.head += 1
            else:
                self.head = 0
            return toReturn
        else:
            raise RuntimeError

    def resize(self, newsize):
        assert (len(self.data) < newsize)
        newQueue = [None] * newsize

        head = self.head
        curr = self.data[head]
        counter = 0

        while curr != None:
            newQueue[counter] = curr
            counter += 1
            if counter != 0 and head == self.tail:
                break
            if head == len(self.data)-1:
                head = 0
            else:
                head += 1
            curr = self.data[head]
        self.tail = counter -1
        self.head = 0
        self.data = newQueue


    def empty(self):
        if self.head == -1 and self.tail == -1:
            return True

        return False


    def __bool__(self):
        return not self.empty()


    def __str__(self):
        if not (self):
            return ''
        return ', '.join(str(x) for x in self)


    def __repr__(self):
        return str(self)


    def __iter__(self):
        head = self.head

        curr = self.data[head]

        while curr != None:
            yield curr
            if head == len(self.data)-1:
                head = 0
            else:
                head += 1
            curr = self.data[head]
