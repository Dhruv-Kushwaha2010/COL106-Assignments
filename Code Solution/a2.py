def pow2(b):                            # helper function which returns 2**b
    if (b == 0):                        # time complexity: O(log(b))
        return 1                        # space complexity: O(1)
    else:                               # recurrence relation: pow2(b) = pow2(b/2)**2 , b is even
        if (b%2 == 0):                  #                      pow2(b) = 2*pow2(b-1) , b is odd
            return pow2(int(b/2))**2    # base case: pow2(0) = 1
        else:
            return 2*pow2(b-1)

def log2(n):                            # helper function which returns log2(n)
    if (n == 1):                        # time complexity: O(log(n))
        return 0                        # space complexity: O(1)
    else:                               # base case: log2(1) = 0
        ans = 0
        while (n > 1):                  # loop invariant: n*(2**ans) is N
            n = int(n/2)                # initialization: ans = 0, n = N, so n*(2**0) = N
            ans += 1                    # maintainence: if n*(2**ans) = N then (n/2)*(2**(ans-1)) = N
        return ans                      # termination: n = 1, 1*(2**ans) = N , therefore ans = log2(N)

# class starts

class priority_queue:                   

    '''
    This class is a special implementation of priority queue (min-heaps) wrt time of collisions, 
    it has been modified according to needs of our problem statement.

    Attributes: 
    
    self._positions : list of float, self._positions[i] is the position of ith particle at the time of last updation 
    self._velocities : list of float, self._velocities[i] is the velocity of ith particle at the time of last updation
    self._collisions : list of tuple(float, float, int), self._collisions[i] contains a tuple of time, position, index respectively.
    self._length : int, length of self._collisions
    self._indexes : list of int, self._indexes[i] is the index of tuple(with index = i) in self._collisions
    self.last_updation_time : list of int, self.last_updation_time[i] contains the time at which the attributes(position, velocity) of ith particle is changed
    

    Methods:

    self.swap(i, j) : swaps the ith and jth element of self._collisions and also swaps the ith and jth element of self._indexes
    self.heap_down(i) : implements the standard heap_down method of min_heaps and prioritize small index in tuple as tie breaker(i.e., small index should be above large index)
    self.heap_up(i) : implements the standard heap_up method of min_heaps and prioritize small index in tuple as tie breaker(i.e., small index should be above large index)
    self.build(list_of_collision_time, list_of_collision_pos) : builds a min heap in O(n) time.
    self.push(time,position,index) : pushes tuple => (time, position, index) in self._collisions
    self.pop() : pops the smallest tuple (wrt time) from self._collisions
    self.size() : size of the self._collisions
    self.index_at_top() : index of smallest element of self._collisions
    self.set_velocity(index, velocity) : assigns self._velocities[index] <-- velocity
    self.set_position(index, position) : assigns self._positions[index] <-- position
    self.top() : returns smallest element of self._collisions
    self.get_velocity(index) : returns self._velocities[index]
    self.get_position(index) : returns self._positions[index]
    self.get_time_of_collisions(i) : returns the time of collision between the particles with indexes i and i+1 by calculation
    self.get_pos_of_collision(i) : returns the position of collision between the particles with indexes i and i+1 by calculation
    self.set_last_updation_time(i,time) : assigns self._last_updation_time[i] <-- time
    self.get_last_updation_time(i) : returns self._last_updation_time[i]
    self.modify_collisions(time, position, i) : assigns the element of self._collisions(which has index i) to (time, position, i) and then applies heap_up and heap_down
    '''
                                         
    def __init__(self,x,v,n):                                       # initializes class 
        self._positions = x
        self._velocities = v
        self._collisions = []
        self._length = 0
        self._indexes = [-1]*(n-1)
        self._last_updation_time = [0]*(n)
        
    def swap(self, i, j):                                           # time complexity O(1), space complexity O(1)
        temp_index_1 = self._collisions[i][2]                       
        temp_index_2 = self._collisions[j][2]
        temp = self._indexes[temp_index_1]
        self._indexes[temp_index_1] = self._indexes[temp_index_2]
        self._indexes[temp_index_2] = temp

        temp1 = self._collisions[i]
        self._collisions[i] = self._collisions[j]
        self._collisions[j] = temp1

    def heap_down(self,i):                                          # time complexity O(log(n)), space complexity O(log(n))
        if (self._length == 0 or self._length == 1):                
            return
        else:
            last_level = log2(self._length)
            while (i < pow2(last_level) - 1):
                
                if (2*i + 2 <= self._length - 1):
                    if (self._collisions[2*i+1][0] < self._collisions[2*i+2][0]):
                        if (self._collisions[i][0] < self._collisions[2*i+1][0]):
                            return
                        elif (self._collisions[i][0] == self._collisions[2*i+1][0]):
                            if (self._collisions[i][1] > self._collisions[2*i+1][1]):
                                self.swap(i,2*i+1)
                            return
                        else:
                            self.swap(i,2*i+1)
                            i = 2*i + 1
                    elif (self._collisions[2*i+1][0] > self._collisions[2*i+2][0]):
                        if (self._collisions[i][0] < self._collisions[2*i+2][0]):
                            return
                        elif (self._collisions[i][0] == self._collisions[2*i+2][0]):
                            if (self._collisions[i][1] > self._collisions[2*i+2][1]):
                                self.swap(i,2*i+2)
                            return
                        else:
                            self.swap(i,2*i+2)
                            i = 2*i + 2
                    else:
                        if (self._collisions[i][0] < self._collisions[2*i+1][0]):
                            return
                        elif (self._collisions[i][0] == self._collisions[2*i+1][0]):
                            if (self._collisions[2*i+1][1] < self._collisions[2*i+2][1]):
                                if (self._collisions[i][1] > self._collisions[2*i+1][1]):
                                    self.swap(i,2*i+1)
                                return
                            else:
                                if (self._collisions[i][1] > self._collisions[2*i+2][1]):
                                    self.swap(i,2*i+2)
                                return
                        else:
                            if (self._collisions[2*i+1][1] < self._collisions[2*i+2][1]):
                                self.swap(i,2*i+1)
                                i = 2*i+1
                            else:
                                self.swap(i,2*i+2)
                                i = 2*i + 2

                elif (2*i + 1 == self._length - 1):
                    if (self._collisions[i][0] > self._collisions[2*i+1][0]):
                        self.swap(i,2*i+1)
                        i = 2*i + 1
                    elif (self._collisions[i][0] == self._collisions[2*i+1][0]):
                        if (self._collisions[i][1] > self._collisions[2*i+1][1]):
                            self.swap(i, 2*i+1)
                        return
                    else:
                        return
                else:
                    return
            return

    def heap_up(self,i):                                            # time complexity O(log(n)), space complexity O(log(n))
        if (self._length == 0 or self._length == 1):                
            return
        else:
            while (i > 0):
                if (self._collisions[int((i-1)/2)][0] > self._collisions[i][0]):
                    self.swap(i,int((i-1)/2))
                    i = int((i-1)/2)
                elif (self._collisions[int((i-1)/2)][0] == self._collisions[i][0]):
                    if (self._collisions[int((i-1)/2)][1] > self._collisions[i][1]):
                        self.swap(i,int((i-1)/2))
                    return
                else:
                    return
            return

    def build(self, lst_of_coll_time, lst_of_coll_pos):             # time complexity O(n), space complexity O(n)
        count = 0                                                    
        for i in range(len(lst_of_coll_time)):
            if (lst_of_coll_time[i] > -1):
                self._indexes[i] = count
                self._collisions.append((lst_of_coll_time[i], lst_of_coll_pos[i], i))
                count += 1
        
        self._length = count
        if (count == 1 or count == 0):
            return
        else:
            last_level = log2(count)
            curr_level = last_level - 1
            while (curr_level >= 0):
                for i in range(pow2(curr_level) - 1, 2*pow2(curr_level) - 1):
                    self.heap_down(i)
                curr_level -= 1
            return

    def push(self,time,pos,ind):                                    # time complexity: O(log(n)), space complexity: O(log(n))
        self._collisions.append((time,pos,ind))
        self._length += 1
        self._indexes[ind] = self._length - 1
        self.heap_up(self._length - 1)

    def pop(self):                                                  # time complexity: O(log(n)), space complexity: O(log(n))
        if (self._length > 1):
            self._indexes[self._collisions[0][2]] = -1
            self._indexes[self._collisions[self._length - 1][2]] = 0
            temp = self._collisions[0]
            self._collisions[0] = self._collisions[self._length - 1]
            self._collisions[self._length - 1] = temp
            self._collisions.pop()
            self._length -= 1
            self.heap_down(0)
        elif (self._length == 1):
            self._indexes[self._collisions[0][2]] = -1
            self._collisions.pop()
            self._length -= 1
        else:
            return

    def size(self):                                                 # time complexity: O(1), space complexity: O(1)
        return self._length

    def index_at_top(self):                                         # time complexity: O(1), space complexity: O(1)
        if (self._length > 0):
            return self._collisions[0][2]

    def set_velocity(self,i,vel):                                   # time complexity: O(1), space complexity: O(1)
        self._velocities[i] = vel

    def set_position(self,i,pos):                                   # time complexity: O(1), space complexity: O(1)
        self._positions[i] = pos

    def top(self):                                                  # time complexity: O(1), space complexity: O(1)
        if (self._length > 0):
            return self._collisions[0]

    def get_velocity(self,i):                                       # time complexity: O(1), space complexity: O(1)
        return self._velocities[i]

    def get_position(self,i):                                       # time complexity: O(1), space complexity: O(1)
        return self._positions[i]

    def get_time_of_collision(self,i):                              # time complexity: O(1), space complexity: O(1)
        if (self._velocities[i] > self._velocities[i+1] and self._positions[i+1] > self._positions[i]):
            return (self._positions[i+1] - self._positions[i])/(self._velocities[i] - self._velocities[i+1])
        else:
            return -1

    def get_pos_of_collision(self,i):                               # time complexity: O(1), space complexity: O(1)
        if (self.get_time_of_collision(i) > 0):
            return (self._positions[i+1]*self._velocities[i] - self._positions[i]*self._velocities[i+1])/(self._velocities[i] - self._velocities[i+1])
        else:
            return 0

    def set_last_updation_time(self,i,time):                        # time complexity: O(1), space complexity: O(1)
        self._last_updation_time[i] = time

    def get_time_of_last_updation(self,i):                          # time complexity: O(1), space complexity: O(1)
        return self._last_updation_time[i]
    
    def modify_collisions(self,time,pos,index):                     # time complexity: O(log(n)), space complexity: O(log(n))
        lst_index = self._indexes[index]
        # print(self._indexes)
        temp = (time, pos, index)
        self._collisions[lst_index] = temp
        
        self.heap_down(lst_index)
        self.heap_up(self._indexes[index])


def listCollisions(M, x, v, m, T):                  # return list of tuples(time, index, position) in dictionary order
    n = len(M)                                      # n : int, M.length
    if (n == 0 or n == 1):                          # base cases
        return []
    else:
        lst_of_collisions = []                      # lst_of_collisions : list of tuples(time, index, position) of collisions in dictionary order
        ob = priority_queue(x, v, n)                # ob : priority_queue of collisions

        initial_lst_of_times = [-1]*(n-1)           # initial_lst_of_times : list of float, contains initial time of collisions
        initial_lst_of_collision_pos = [0]*(n-1)    # initial_lst_of_collisions_pos : list of float, contains position of next collision

        for i in range(n-1):                        # assigns the respective values to initial_lst_of_times, initial_lst_of_collisions_pos according to the following formulaes
                                                    # t = (x[i+1] - x[i])/(v[i] - v[i+1]) and pos = (x[i+1]*v[i] - x[i]*v[i+1])/(v[i] - v[i+1])
            if (v[i] > v[i+1]):                    
                initial_lst_of_times[i] = (x[i+1] - x[i])/(v[i] - v[i+1])
                initial_lst_of_collision_pos[i] = (x[i+1]*v[i] - x[i]*v[i+1])/(v[i] - v[i+1])
        
        ob.build(initial_lst_of_times, initial_lst_of_collision_pos)    # builds the initial priority_queue
        absolute_time = 0                                               # absolute_time : float, starts with t = 0 denotes the time elapsed
        
        while (ob.size() > 0 and m > 0 and absolute_time <= T):         # while number of collisions completed are less than m or time elapsed is less than T

            curr_collision = ob.top()               # tuple of (time, position, index) of the current collision
            curr_index = curr_collision[2]          # int, index of the left particle(particle with lesser value of x) involved in the current collision

            absolute_time = curr_collision[0]       # as per definition of time stored in curr_collision

            if (absolute_time > T):                 # as per conditions provided in the problem statement
                break
                
            m -= 1                                  # as per conditions provided in the problem statement
            
            ob.set_position(curr_index, curr_collision[1])                              # updates the position of left particle involved in current collision
            ob.set_position(curr_index+1, curr_collision[1])                            # updates the position of right particle involved in current collision

            ob.set_last_updation_time(curr_index, absolute_time)                        # updates the time of left particle involved in current collision
            ob.set_last_updation_time(curr_index+1, absolute_time)                      # updates the time of right particle involved in current collision
            v1 = ob.get_velocity(curr_index)                                            # v1 : float, velocity of left particle before collision
            v2 = ob.get_velocity(curr_index+1)                                          # v2 : float, velocity of right particle before collision
            tempv = v1                                                                  # tempv : float, temporary variable 
            v1 = (2*M[curr_index+1]*v2 + (M[curr_index] - M[curr_index+1])*v1)/(M[curr_index] + M[curr_index+1])    # v1 : float, velocity of left particle after collision
            v2 = (2*M[curr_index]*tempv + (M[curr_index+1] - M[curr_index])*v2)/(M[curr_index] + M[curr_index+1])   # v2 : float, velocity of right particle after collision
            ob.set_velocity(curr_index,v1)                                              # updates the velocity of left particle
            ob.set_velocity(curr_index+1, v2)                                           # updates the velocity of right particle
            lst_of_collisions.append((absolute_time,curr_index, curr_collision[1]))     # adds the current collision in the lst_of_collisions
            ob.pop()                                                                    # removes the node containing the current_collision from ob._collisions

        
            # this block updates the attributes related to curr_index - 1 particle 
            if (curr_index - 1 >= 0):               
                if (ob._indexes[curr_index - 1] == -1):
                    if (ob.get_velocity(curr_index-1) > ob.get_velocity(curr_index)):
                        
                        ob.set_position(curr_index-1, ob.get_position(curr_index-1) + ob.get_velocity(curr_index-1)*(absolute_time - ob.get_time_of_last_updation(curr_index-1)))
                        new_time = ob.get_time_of_collision(curr_index-1)
                        new_pos = ob.get_pos_of_collision(curr_index - 1)
                        ob.push(absolute_time + new_time, new_pos, curr_index - 1)
                        ob.set_last_updation_time(curr_index-1, absolute_time)
                else:
                    if (ob.get_velocity(curr_index-1) > ob.get_velocity(curr_index)):
                        ob.set_position(curr_index-1, ob.get_position(curr_index-1) + ob.get_velocity(curr_index-1)*(absolute_time - ob.get_time_of_last_updation(curr_index-1)))
                        new_time = ob.get_time_of_collision(curr_index - 1)
                        new_pos = ob.get_pos_of_collision(curr_index-1)
                        ob.modify_collisions(absolute_time + new_time, new_pos, curr_index-1)
                        ob.set_last_updation_time(curr_index-1, absolute_time)
                  
            # this block updates the attributes related to curr_index + 2 particle 
            if (curr_index + 2 <= n - 1):
                if (ob._indexes[curr_index + 1] == -1):
                    if (ob.get_velocity(curr_index+1) > ob.get_velocity(curr_index+2)):
                        ob.set_position(curr_index+2, ob.get_position(curr_index + 2) + ob.get_velocity(curr_index+2)*(absolute_time - ob.get_time_of_last_updation(curr_index + 2)))
                        new_time = ob.get_time_of_collision(curr_index + 1)
                        new_pos = ob.get_pos_of_collision(curr_index + 1)
                        ob.push(absolute_time + new_time, new_pos, curr_index + 1)
                        ob.set_last_updation_time(curr_index+2, absolute_time)
                else:
                    if (ob.get_velocity(curr_index+1) > ob.get_velocity(curr_index+2)):
                        ob.set_position(curr_index+2, ob.get_position(curr_index + 2) + ob.get_velocity(curr_index+2)*(absolute_time - ob.get_time_of_last_updation(curr_index + 2)))
                        new_time = ob.get_time_of_collision(curr_index + 1)
                        new_pos = ob.get_pos_of_collision(curr_index + 1)
                        ob.modify_collisions(absolute_time + new_time, new_pos, curr_index + 1)
                        ob.set_last_updation_time(curr_index+2, absolute_time)

        
        return lst_of_collisions    # returns final list of collisions