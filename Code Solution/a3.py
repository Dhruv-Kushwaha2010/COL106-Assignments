class Node:                         #? This class is the node of the tree of PointDatabase

    def __init__(self):
        self._xmin = None           #* minimum x amoung the set of points stored at this Node
        self._xmax = None           #* maximum x amoung the set of points stored at this Node
        self._yList = []            #* List of points stored at this Node sorted in y
        self._left = None           #* Left Child of this Node
        self._right = None          #* Right Child of this Node


class PointDatabase(Node):          
    #? Attributes: _pointList: stores all the location of restaurants and is sorted in x
    #?             _PointDatabase: root Node of the Datastructure Implemented

    #? Methods: buildPointDatabase(List): returns the root Node of the Datastructure used to store the list of points
    #?          preorderTraversal(rootNode): returns the list of preorder traversal of this tree
    #?          searchNearby(self, q, d): returns all the points in Datastructure which are at a distance of d from q


    def __init__(self, pointList):
        self._pointList = pointList
        self._pointList.sort(key = lambda x: x[0])                                   #* Sorting the pointList in x
        self._PointDatabase = PointDatabase.buildPointDatabase(self._pointList)         

    def buildPointDatabase(List):
        return PointDatabase.buildPointDatabaseHelper(List)

    def buildPointDatabaseHelper(List):                     #? Helper function(Recurrsive), returns a Node containing List in the Datastructure
        if (len(List) > 0):
            currNode = Node()
            currNode._xmin = List[0][0]
            currNode._xmax = List[-1][0]

            if (len(List) == 1):                            #? If this currNode is a Leaf of this Tree
                currNode._yList = List
                return currNode

            else:                                   #* else -> len(List) > 1, Therefore Nodes here are not Leaves and have two childs
                currNode._left = PointDatabase.buildPointDatabaseHelper(List[:(len(List)//2)])      #? Recurrsively building left child node
                currNode._right = PointDatabase.buildPointDatabaseHelper(List[(len(List)//2):])     #? Recurrsively building right child node
                
                currNode._yList = PointDatabase.mergeList(currNode._left._yList, currNode._right._yList)    #? yList of Node is the addition of its childs sorted yList
                
                return currNode
        else:
            return None             #? If the List is empty


    def mergeList(List1, List2):        #? Merges two sorted Lists into a sorted List in O(m+n) time complexity 
        List = []
        i1 = 0
        i2 = 0
        cnt = 0
        while (cnt < (len(List1) + len(List2))):
            cnt += 1
            if ((i1 < len(List1)) and (i2 < len(List2))):
                
                if (List1[i1][1] < List2[i2][1]):
                    List.append(List1[i1])
                    i1 += 1
                else:
                    List.append(List2[i2])
                    i2 += 1
            else:
                if (i1 < len(List1)):
                    List.append(List1[i1])
                    i1 += 1
                else:
                    List.append(List2[i2])
                    i2 += 1
        return List

    def preorderTraversal(rootNode):                                #? Returns a list of preorder Traversal of the Tree of Datastructure Implemented
        return PointDatabase.preorderTraversalHelper(rootNode, [])      #? calling helper function , initially list of Preorder Traversal is empty

    def preorderTraversalHelper(currNode,List):         #? Merges the list of preorder traversal of subtree of the currNode in given List
        if (currNode is None):                          #? If currNode is None, subtree is empty
            return List

        else:                                           #? If currNode is not None, it is a Leaf or it has atleast two childs
            List.append((currNode._xmin, currNode._xmax, currNode._yList))          #? Preorder Traversal contains (_xmin, _xmax, _yList) of every Node in Preorder

            if (currNode._left is not None):            #? If left child is not None, recursively calling its preorder Traversal(Note: left child might be a leaf)
                List = PointDatabase.preorderTraversalHelper(currNode._left, List)
            
            if (currNode._right is not None):           #? If right child is not None, recursively calling its preorder Traversal(Note: right child might be a leaf)
                List = PointDatabase.preorderTraversalHelper(currNode._right, List)
                                                        
            return List         #? return the List which which contains the attributes of currNode, preorder Traversal of subtree of left and right child.

    def searchNearby(self, q, d):       #? Returns a list of points at less than a distance d from q in the Datastructure
        if (d == 0):                    #? If d is 0, then there are no such points 
            return []                   #? Therefore return empty list

        else:                           #? else -> (d > 0)
            return PointDatabase.searchNearbyHelper(self._PointDatabase, (q[0]-d, q[0]+d), (q[1]-d, q[1]+d), [])        #? Calling helper function

    def searchNearbyHelper(currNode, x_range, y_range, List):   #? Merges the list of points at a distance less than equal to d from q in the subtree of currNode to given List
        if (currNode is not None):                      #? subTree of currNode is not empty
            if (len(currNode._yList) == 1):             #? If currNode is leaf
                if (currNode._xmin >= x_range[0]) and (currNode._xmin <= x_range[1]) and (currNode._yList[0][1] >= y_range[0]) and (currNode._yList[0][1] <= y_range[1]):
                                                        #? If currNode satisfies the conditions
                    List.append(currNode._yList[0])     #? Add it in List
                else:                                   #? else return the List
                    return List
                return List
            else:                                       #? else -> currNode has at least 2 childs
                if (currNode._xmin >= x_range[0]) and (currNode._xmax <= x_range[1]):       #? All points are completely contained in x
                    List = PointDatabase.binarySearch(currNode._yList, y_range, List)       #? Then, calling binarySearch in y (Note: _yList contains at least 2 elements)
            
                elif (currNode._xmax >= x_range[0]) and (currNode._xmin <= x_range[1]):     #? If partially contained then recurrsively call left child and right child
                                                                                            #! Note: Here at least one intersection in x must be present
                    List = PointDatabase.searchNearbyHelper(currNode._left, x_range, y_range, List)     #! Also left and right childs might be leafs
                    List = PointDatabase.searchNearbyHelper(currNode._right, x_range, y_range, List)
                return List         #? Return the List
        else:
            return List             #? If currNode is empty, simply return the given List

    def binarySearch(yList, y_range, List):         #? Adds the list of points(that satisfies y's range condition) in the given List
                                                                                #! yList contains atleast 2 elements and yList is sorted in y

        if (yList[-1][1] <= y_range[0]):        #? if there is no element in range or only the last element of the yList is in range
            if (yList[-1][1] == y_range[0]):    #? if Only the last element of the yList is in the range
                List.append(yList[-1])          #? Add it in the given List
                return List                     #? return List
            
            else:                               #? If there is no element in range
                return List                     #? Simply return given List
        
        else:                                   #! There is at least 1 elements in yList which is greater than or equal to y_min
            if (yList[0][1] >= y_range[1]):     #? if there is no element is range or only the first element of the yList is in range
                if (yList[0][1] == y_range[1]): #? if only first element of the yList is in the range
                    List.append(yList[0])       #? Add that element to the given List
                    return List                 #? return List
                
                else:                           #? If there is no element in range
                    return List                 #? Simply return given List

            else:                                           #! There is at least 1 element in yList which is less than or equal to y_max
                if (y_range[0] <= yList[0][1]):             #? If y_min is less than or equal to first element of yList
                    lowerBoundIndex = 0                     
                    if (y_range[1] >= yList[-1][1]):        #? If y_max is more than or equal to last element of yList
                        upperBoundIndex = len(yList) - 1

                    else:                       #? else -> upperBoundIndex exists and is in range (1,len(yList) - 1)
                        upperBoundIndex = PointDatabase.binarySearchHelperUpperIndex(yList, y_range[1])     #! Note: upperBoundIndex is not at first or last element, it is in between them   
                else:                                       #? else -> y_min is in range (1, len(yList) - 1)
                    lowerBoundIndex = PointDatabase.binarySearchHelperLowerIndex(yList, y_range[0])         #! Note: lowerBoundIndex is not at first or last element, it is in between them
                    if (y_range[1] >= yList[-1][1]):        #? If y_max is more than equal to last element of yList
                        upperBoundIndex = len(yList) - 1
                    
                    else:                       #? else -> upperBoundIndex exists and is in range (1, len(yList) - 1)
                        upperBoundIndex = PointDatabase.binarySearchHelperUpperIndex(yList, y_range[1])     #! Note: upperBoundIndex is not at first or last element, it is in between them

        List = PointDatabase.mergeList(List, yList[lowerBoundIndex: upperBoundIndex+1])
        return List                                                                             #? Return the merged List


    def binarySearchHelperLowerIndex(yList, y_min):         #! Note: yList contains at least 3 elements
                                                            #! Note: yList is in range(1, len(yList) - 1) 
          
        currLowerBound = 0
        currUpperBound = len(yList) - 1
        i = (currLowerBound + currUpperBound)//2                            #? i is initially pointing at the median of yList (i is at least 1 initially) 
        while ((yList[i+1][1] <= y_min) or (yList[i][1] > y_min)):          #! i should be less than n-1
            i = (currLowerBound + currUpperBound)//2                        #? i is the median of the current subList

            if (yList[i][1] > y_min):                                       #? if y_min is in left of current median
                currUpperBound = (currLowerBound + currUpperBound)//2       #? reduce the upperBound of current subList

            else:                                                           #? else -> y_min is in right of current median
                currLowerBound = (currLowerBound + currUpperBound)//2       #? increase the upperBound of current median
                    
        if (yList[i][1] == y_min):                                          #? if element at i is equal to y_min
            return i                                                        #? return i
        
        else:                                                               #? yList[i] is smaller than y_min               
            return i+1                                                      #? return i+1


    def binarySearchHelperUpperIndex(yList, y_max):         #! Note: yList contains at least 3 elements
                                                            #! Note: yList is in range(1, len(yList) - 1)
 
        currLowerBound = 0
        currUpperBound = len(yList) - 1
        i = (currLowerBound + currUpperBound)//2                            #? i is initially pointing at the median of yList (i is atleast 1 initially)

        while ((yList[i][1] > y_max) or (yList[i+1][1] <= y_max)):          #! i should be less than n-1
            i = (currLowerBound + currUpperBound)//2                        #? i is always at median of current subList

            if (yList[i][1] > y_max):                                       #? if yList[i] is more than y_max
                currUpperBound = (currLowerBound + currUpperBound)//2       #? Then, Reduce the upperBound of subList

            else:                                                           #? if yList[i] is less than y_max
                currLowerBound = (currLowerBound + currUpperBound)//2       #? Then, Increase the lowerBound of subList

        return i
        