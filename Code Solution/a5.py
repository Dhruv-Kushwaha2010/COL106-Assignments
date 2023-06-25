class priorityQueue:                                        #? datastructure, contains tuples of 3 elements(weight, id, prev)
    def __init__(self):                                     #? attributes: q(level-order traversal of the priority queue)
        self.q = []
        
    def swap(self, i, j):                                   #? swaps two elements at indices i and j in q
        self.q[i], self.q[j] = self.q[j], self.q[i]

    def heap_down(self, i):                                 #? brings the curr_node to its appropriate position by swapping it by its childrens
        l = len(self.q)                                     # length of q
        while (2*i + 1 < l):                                #? child of ith curr_node exists
            if (2*i + 2 < l):                               #? curr_node has 2 childs
                if (self.q[2*i+1][0] > self.q[2*i+2][0]):   #? left child is larger than right child
                    if (self.q[2*i+1][0] > self.q[i][0]):   #? left child is larger than its parent
                        priorityQueue.swap(self, i, 2*i+1)
                        i = 2*i+1
                        continue
                    else:                                   #? largest child is smaller than its parent
                        break
                else:                                       #? right child is larger than or equal to left child
                    if (self.q[2*i+2][0] > self.q[i][0]):   #? right child is larger than its parent
                        priorityQueue.swap(self, i, 2*i+2)
                        i = 2*i+2
                        continue
                    else:                                   #? largest child is smaller than its parent
                        break
            else:                                           #? curr_node has only 1 child
                if (self.q[2*i+1][0] > self.q[i][0]):       #? left child is larger than its parent
                    priorityQueue.swap(self, i, 2*i+1)
                break                                       # this was at most the last swap
        return

    def heap_up(self, i):                                   #? brings the curr_node to its appropriate position by swapping it by its parent
        while(int((i-1)/2) >= 0):                           #? parent of curr_node exists
            j = int((i-1)/2)                                # index of parent of curr_node
            if (self.q[j][0] < self.q[i][0]):               #? parent of curr_node is smaller
                priorityQueue.swap(self, i, j)
                i = j
                continue
            else:                                           #? parent of curr_node is bigger
                break
        return

    def push(self, val):                                    #? add an element val to the priority queue
        self.q.append(val)                                  
        priorityQueue.heap_up(self, len(self.q)-1)
        return

    def pop(self):                                          #? pops the maximum element of q
        if (len(self.q) == 0):                              #? q is empty 
            return
        else:                                               #? q is not empty
            priorityQueue.swap(self, 0, -1)                 
            self.q.pop()
            priorityQueue.heap_down(self, 0)
            return

    def top(self):                                          #? returns the element with highest weightage
        if (len(self.q) != 0):                              
            return self.q[0]

    def is_empty(self):                                     #? returns true if self.q is empty else returns false
        return (len(self.q) == 0)    

def findMaxCapacity(n, links, s, t):                                            #? finds the maximum capacity that can be send from s to t
    adj = dict()                                                                # dictionary of dictionary that stores capacity of links
    visited = []                                                                # list of size n, bool, true iff vertex is visited
    prev = []                                                                   # list of size n, stores prev vertex of each vertex
    for i in range(n):                                                          #? initializing visited, prev, adj
        visited.append(False)
        prev.append(-1)
        adj[i] = dict()
    for link in links:                                                          #? computing adj from given links
        if (link[1] in adj[link[0]].keys()):                                    #? if a link already exists
            adj[link[0]][link[1]] = max(link[2], adj[link[0]][link[1]])
        else:                                                                   #? if a link doesn't already exists
            adj[link[0]][link[1]] = link[2]
        if (link[0] in adj[link[1]].keys()):                                    #? if a link already exists
            adj[link[1]][link[0]] = max(link[2], adj[link[1]][link[0]])
        else:                                                                   #? if a link doesn't already exists
            adj[link[1]][link[0]] = link[2] 
    q = priorityQueue()                                                         # priority queue; (maximum capcity path, vertex)
    q.push((float("inf"), s, -1))                                               # enqueue s into q 
    while (not q.is_empty()):                                                   #? runs till q is empty
        curr = q.top()                                                          # current vertex
        prev[curr[1]] = curr[2]                                                 # computing prev for current vertex
        q.pop()                                                                 # pop current vertex from the priority queue
        visited[curr[1]] = True                                                 # set visited to True
        if (curr[1] == t):                                                      #? already done => break
            break
        for adj_vertex in adj[curr[1]]:                                         #? enqueue all the unvisited neighbours of curr_vertex in q
            if (visited[adj_vertex]):
                continue
            q.push((min(curr[0], adj[curr[1]][adj_vertex]), adj_vertex, curr[1]))
    i = t
    path = []                                                                   # final optimum path from s to t
    while(prev[i] >= 0):                                                        #? computing path
        i = prev[i]
        path.append(i)
    path.reverse()
    path.append(t)
    return(curr[0], path)