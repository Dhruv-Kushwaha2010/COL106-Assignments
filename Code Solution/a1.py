# "Node" class here is an object which contains three objects , namely: key, next, previous.
# key: is the value stored in that node.
# next: is an object that stores reference to the next node.
# previous: is an object that stores reference to the previous node. 
class Node(object):

    # the initializer function can take the key value of the node as input
    def __init__(self, key = None):
        self._key = key
        self._next = None
        self._previous = None

    # set_next links a new node in front of the current node
    def set_next(self,new_node):
        self._next = new_node
        new_node._previous = self

    # get_next returns the next node
    def get_next(self):
        return self._next

    # set_previous links a new node behind the current node
    def set_previous(self, new_node):
        self._previous = new_node
        new_node._next = self

    # get_previous return the previous node
    def get_previous(self):
        return self._previous

    # get_key returns the key(data) stored in the current node
    def get_key(self):
        return self._key

# code for testing the Node class

# if __name__ == "__main__":
#     root_node = Node(1)
#     first_node = Node(2)
#     second_node = Node(3)
#     first_node.set_next(second_node)
#     first_node.set_previous(root_node)
#     print(first_node._next.get_key())
#     # output should be 3

# "stack" class is an object which has the attributes and methods of the data structure --> "stack"
class stack(object):

    # initializer function creates a node for the object(stack),
    # this node("curr_node") always points at the last node of the stack
    # if the stack is empty, it points at "None"
    def __init__(self):
        self._curr_node = Node()
        self._length = 0

    # push function pushes a value(val) at the end of the stack
    def push(self, val):
        if (self._length == 0):
            self._new_node = Node(val)
            self._curr_node._next = self._new_node

        else:
            self._new_node = Node(val)
            Node.set_next(self._curr_node._next, self._new_node)
            self._curr_node._next = self._new_node
        self._length += 1

    # pop function removes the last element from the stack
    # pop function returns the key of the last element 
    def pop(self):
        if (self._length == 0):
            return "stack is empty"
        elif (self._length == 1):
            self._curr_node = Node()
            self._length -= 1
        else:
            self._last_element = self._curr_node._next._key
            self._curr_node._next = self._curr_node._next._previous
            self._curr_node._next._next = None
            self._length -= 1
            return self._last_element

    # length function returns the length of the stack
    def length(self):
        return self._length

    # end_key function returns the value of the last element of stack
    def last(self):
        return self._curr_node._next._key


# code for testing the "stack" class

# if (__name__ == "__main__"):
#     pile = stack()
#     pile.push(1)
#     pile.push(2)
#     print(pile.last())
#     print(pile.pop())
#     print(pile.last())
#     print(pile.length())
#     pile.pop()
#     pile.pop()

# the main starts here

# findPositionandDistance returns a list that contains [x,y,z,d] of the final position
def findPositionandDistance(P):
    n = len(P) # n is the length of the input string(S)
    x = 0 # x is the x-coordinate of the final position of drone
    y = 0 # y is the y-coordinate of the final position of drone
    z = 0 # z is the z-coordinate of the final position of drone
    d = 0 # d is the distance travelled by the drone till it reaches the final position
    multiplier = stack() # multiplier is a 'stack' which contains the numbers which we multiply to the commands
    num_str = '' # num_str is current string of numbers in command
    sign = 1 # sign denotes the + or - sign in command
    i = 0 # i is the iterator for the while loop
    while (i < n):

        if (P[i].isnumeric()):
            while(i < n):
                if (P[i].isnumeric()):
                    num_str = num_str + P[i]
                else:
                    break
                i += 1
            if (multiplier.length() > 0):
                multiplier.push((multiplier.last())*int(num_str))
            else:
                multiplier.push(int(num_str))
            num_str = ''

        elif (P[i] == '('):
            continue

        elif (P[i] == ')'):
            multiplier.pop()

        elif (P[i] == '+'):
            sign = 1

        elif (P[i] == '-'):
            sign = -1

        elif (P[i] == 'X'):
            if (multiplier.length() == 0):
                x += sign
                d += 1
            else:
                x += (multiplier.last())*(sign)
                d += (multiplier.last())

        elif (P[i] == 'Y'):
            if (multiplier.length() == 0):
                y += sign
                d += 1
            else:
                y += (multiplier.last())*(sign)
                d += (multiplier.last())

        elif (P[i] == 'Z'):
            if (multiplier.length() == 0):
                z += sign
                d += 1
            else:
                z += (multiplier.last())*(sign)
                d += (multiplier.last())

        i += 1

    final_lst = [x,y,z,d]
    return final_lst

# sample test_cases

# if __name__ == "__main__":
#     print(findPositionandDistance("+X+Y+X-Y-Z+X+X-Z-Z-Z-Z-Y+Y-X"))
#     print(findPositionandDistance("+X2(+Y-X-Z)8(+Y)9(-Z-Z)"))
#     print(findPositionandDistance(""))
#     print(findPositionandDistance("5(2(3(+X+X)))"))
#     print(findPositionandDistance("+Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))"))
#     print(findPositionandDistance("1(+X)5(+Y)41(+Z)1805(-X)3263441(-Y)10650056950805(-Z)"))
#     print(findPositionandDistance("0(+X)"))
        
            

        

