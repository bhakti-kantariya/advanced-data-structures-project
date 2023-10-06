import sys
import re

#hashmap to maintain the pointer to the min heap 
ridePointers = dict()

#open a output file
with open("output_file.txt", "w") as f:

    #min heap implementation
    class MinHeap:
        def __init__(self, maxtreesize):
            self.maxtreesize = maxtreesize
            self.leafride = 0
            self.Heap = [[sys.maxsize, sys.maxsize, sys.maxsize] for _ in range(self.maxtreesize + 1)]
            self.Heap[0] = [-1 * sys.maxsize,-1 * sys.maxsize,-1 * sys.maxsize]
            self.ROOTNODE = 1
            global ridePointers
        #gives the location of parent of the current node at loc
        def parentRide(self, loc):
            return loc//2
        #gives the location of leftchild of the current node at loc
        def leftChild(self, loc):
            return 2 * loc
        #gives the location of rightchild of the current node at loc
        def rightChild(self, loc):
            return (2 * loc) + 1
        #to check if the node at loc is a leaf node
        def isLeafRideNode(self, loc):
            return loc*2 > self.leafride
        #swaps the ride nodes at floc and sloc
        def swaprides(self, floc, sloc):
            self.Heap[floc], self.Heap[sloc] = self.Heap[sloc], self.Heap[floc]
            ridePointers[self.Heap[floc][0]], ridePointers[self.Heap[sloc][0]] = ridePointers[self.Heap[sloc][0]], ridePointers[self.Heap[floc][0]]
        #heapifies the tree with root at loc
        def minRideHeapify(self, loc):
            if not self.isLeafRideNode(loc):
                #checks if the ridecost of parent is greater than its childs
                if (self.Heap[loc][1] > self.Heap[self.leftChild(loc)][1] or self.Heap[loc][1] > self.Heap[self.rightChild(loc)][1]):
                    #swaps the leftchild with parent if the ridecost of left child is less than parent ridecost
                    if self.Heap[self.leftChild(loc)][1] < self.Heap[self.rightChild(loc)][1]:
                        self.swaprides(loc, self.leftChild(loc))
                        self.minRideHeapify(self.leftChild(loc))
                    #swaps the rightchild with parent if the ridecost of right child is less than parent ridecost
                    else:
                        self.swaprides(loc, self.rightChild(loc))
                        self.minRideHeapify(self.rightChild(loc))
                #checks if both the child rides have ridecost same as the parent's ridecost
                if (self.Heap[loc][1] == self.Heap[self.leftChild(loc)][1] and self.Heap[loc][1] == self.Heap[self.rightChild(loc)][1]):
                    #swap the child ride with th parent who's tripduration is minimum
                    if self.Heap[self.leftChild(loc)][2] < self.Heap[self.rightChild(loc)][2]:
                        self.swaprides(loc, self.leftChild(loc))
                        self.minRideHeapify(self.leftChild(loc))
                    else:
                        self.swaprides(loc, self.rightChild(loc))
                        self.minRideHeapify(self.rightChild(loc))
                #check if the ridecost of parent and left child ride is same and trip duration of left child ride is less than the parent
                if (self.Heap[loc][1] == self.Heap[self.leftChild(loc)][1] and self.Heap[loc][2] > self.Heap[self.leftChild(loc)][2]):
                        self.swaprides(loc, self.leftChild(loc))
                        self.minRideHeapify(self.leftChild(loc))
                #check if the ridecost of parent and right child ride is same and trip duration of right child ride is less than the parent
                elif (self.Heap[loc][1] == self.Heap[self.rightChild(loc)][1] and self.Heap[loc][2] > self.Heap[self.rightChild(loc)][2]):
                        self.swaprides(loc, self.rightChild(loc))
                        self.minRideHeapify(self.rightChild(loc))

        #performs insertion of a node with [rideNumber, rideCost, tripDuration] in min heap
        def insertMHeap(self, rideNumber, rideCost, tripDuration):

            if self.leafride >= self.maxtreesize :
                return
            #add new ride to the leafride and increment leafride
            self.leafride+= 1
            self.Heap[self.leafride] = [rideNumber, rideCost, tripDuration]
            ridePointers[rideNumber] = self.leafride
            current = self.leafride
            #swap the rides until parent of new ride has less ridecost
            while self.Heap[current][1] < self.Heap[self.parentRide(current)][1]:
                self.swaprides(current, self.parentRide(current))
                current = self.parentRide(current)
            #swap the rides until parent of new ride has same ridecost but has less tripduration
            while self.Heap[current][1] == self.Heap[self.parentRide(current)][1] and self.Heap[current][2]<self.Heap[self.parentRide(current)][2]:
                self.swaprides(current, self.parentRide(current))
                current = self.parentRide(current)
    
        #returns the root of the min heap and deletes it from the heap
        def getNextRide(self):
            popped = self.Heap[self.ROOTNODE]
            if popped[0] != -1 * sys.maxsize:
                del ridePointers[self.Heap[self.ROOTNODE][0]]
                if self.leafride>1:
                    self.Heap[self.ROOTNODE] = self.Heap[self.leafride]
                    ridePointers[self.Heap[self.ROOTNODE][0]] = self.ROOTNODE
                    self.leafride-= 1
                    self.minRideHeapify(self.ROOTNODE)
                else:
                    self.Heap[self.ROOTNODE] = [-1 * sys.maxsize,-1 * sys.maxsize,-1 * sys.maxsize]
                    self.leafride-= 1
                return popped
            else:
                return 
        
        #deletes the ride at location and replaces it with last node of tree and then performs heapify
        def cancelRide(self, location):
            del ridePointers[self.Heap[location][0]]
            if location != self.leafride:
                self.Heap[location] = self.Heap[self.leafride]
                ridePointers[self.Heap[location][0]] = location
                self.minRideHeapify(location)
            else:
                self.Heap[location] = [-1 * sys.maxsize,-1 * sys.maxsize,-1 * sys.maxsize]
            self.leafride-=1
        
        #updates the ride tripduration based on the value of newTripDuration
        def updateTrip(self, location, newTripDuration):
            if newTripDuration <= self.Heap[location][2]:
                self.Heap[location][2] = newTripDuration
                self.minRideHeapify(self.ROOTNODE)
            elif self.Heap[location][2] < newTripDuration and newTripDuration <= 2*self.Heap[location][2]:
                self.Heap[location][1] = self.Heap[location][1]+10
                self.Heap[location][2] = newTripDuration
                self.minRideHeapify(self.ROOTNODE)
            elif newTripDuration > 2*self.Heap[location][2]:
                self.cancelRide(location)

    #node class for red black tree
    class RideNode():
        def __init__(self,rideNumber,rideCost,tripDuration):       
            self.rideNumber = rideNumber
            self.rideCost = rideCost
            self.tripDuration = tripDuration
            self.leftChild = None
            self.rightChild = None
            self.parentRide = None
            self.nodecolor = 'R'

    #red black tree implementation
    class RedBlackTree():
        def __init__(self, minheapInstance):
            self.TNULL = RideNode(0,0,0)
            self.TNULL.nodecolor = 'B'
            self.TNULL.leftChild = None
            self.TNULL.rightChild = None
            self.TNULL.rideNumber = 0
            self.TNULL.rideCost = 0
            self.TNULL.tripDuration = 0
            self.root = self.TNULL
            self.minheapInstance = minheapInstance
            global ridePointers
        
        #inserts a node into red black tree 
        def insertRBT(self, rideNumber, rideCost, tripDuration):
            if rideNumber in ridePointers:
                print("Duplicate RideNumber", end="", file=f)
                exit()
            ride = RideNode(rideNumber, rideCost, tripDuration)
            ride.parentRide = None
            ride.rideNumber = rideNumber
            ride.rideCost = rideCost
            ride.tripDuration = tripDuration
            ride.leftChild = self.TNULL
            ride.rightChild = self.TNULL
            ride.nodecolor = 'R'

            leafRide = None
            rootRide = self.root
            while rootRide != self.TNULL:
                leafRide = rootRide
                if ride.rideNumber < rootRide.rideNumber:
                    rootRide = rootRide.leftChild
                else:
                    rootRide = rootRide.rightChild

            ride.parentRide = leafRide
            if leafRide == None:
                self.root = ride
            elif ride.rideNumber < leafRide.rideNumber:
                leafRide.leftChild = ride
            else:
                leafRide.rightChild = ride

            if ride.parentRide == None:
                ride.nodecolor = 'B'
                return

            if ride.parentRide.parentRide == None:
                return

            self.rotationAndRecoloring_insertRBT(ride)
        
        #rotates and recolors after insertion of a new node
        def rotationAndRecoloring_insertRBT(self, ride):
            while ride.parentRide.nodecolor == 'R':
                if ride.parentRide == ride.parentRide.parentRide.rightChild:
                    parentSiblingRide = ride.parentRide.parentRide.leftChild
                    if parentSiblingRide.nodecolor == 'R':
                        parentSiblingRide.nodecolor = 'B'
                        ride.parentRide.nodecolor = 'B'
                        ride.parentRide.parentRide.nodecolor = 'R'
                        ride = ride.parentRide.parentRide
                    else:
                        if ride == ride.parentRide.leftChild:
                            ride = ride.parentRide
                            self.r_rotation(ride)
                        ride.parentRide.nodecolor = 'B'
                        ride.parentRide.parentRide.nodecolor = 'R'
                        self.l_rotation(ride.parentRide.parentRide)
                else:
                    parentSiblingRide = ride.parentRide.parentRide.rightChild

                    if parentSiblingRide.nodecolor == 'R':
                        parentSiblingRide.nodecolor = 'B'
                        ride.parentRide.nodecolor = 'B'
                        ride.parentRide.parentRide.nodecolor = 'R'
                        ride = ride.parentRide.parentRide
                    else:
                        if ride == ride.parentRide.rightChild:
                            ride = ride.parentRide
                            self.l_rotation(ride)
                        ride.parentRide.nodecolor = 'B'
                        ride.parentRide.parentRide.nodecolor = 'R'
                        self.r_rotation(ride.parentRide.parentRide)
                if ride == self.root:
                    break
            self.root.nodecolor = 'B'
        
        #performs L - left rotation
        def l_rotation(self, ride):
            siblingRide = ride.rightChild
            ride.rightChild = siblingRide.leftChild
            if siblingRide.leftChild != self.TNULL:
                siblingRide.leftChild.parentRide = ride

            siblingRide.parentRide = ride.parentRide
            if ride.parentRide == None:
                self.root = siblingRide
            elif ride == ride.parentRide.leftChild:
                ride.parentRide.leftChild = siblingRide
            else:
                ride.parentRide.rightChild = siblingRide
            siblingRide.leftChild = ride
            ride.parentRide = siblingRide

        #performs R- right rotation
        def r_rotation(self, ride):
            siblingRide = ride.leftChild
            ride.leftChild = siblingRide.rightChild
            if siblingRide.rightChild != self.TNULL:
                siblingRide.right.parentRide = ride

            siblingRide.parentRide = ride.parentRide
            if ride.parentRide == None:
                self.root = siblingRide
            elif ride == ride.parentRide.rightChild:
                ride.parentRide.rightChild = siblingRide
            else:
                ride.parentRide.leftChild = siblingRide
            siblingRide.rightChild = ride
            ride.parentRide = siblingRide

        #print single triplet and multiple triplets in range from rideNumberFrom to rideNumberTo
        def print_ride(self, rideNumberFrom, rideNumberTo=None):
            #to print only single triplet, setting rideNumberFrom and rideNumberTo to rideNumber
            if rideNumberTo == None: rideNumberTo = rideNumberFrom
            rideDetails = []
            self.print_ride_helper(self.root, rideNumberFrom, rideNumberTo, rideDetails)
            if rideDetails:
                finalrides = ""
                for rideDetail in rideDetails:
                    finalrides = finalrides+rideDetail+","
                print(finalrides[:-1], file=f)
            else:
                print('(0,0,0)', file=f)
        
        #finds the rides with rideNumber and between rideNumberFrom and rideNumberTo
        def print_ride_helper(self, ride, rideNumberFrom, rideNumberTo, rideDetails):
            if ride == self.TNULL:
                return
            if rideNumberFrom < ride.rideNumber:
                self.print_ride_helper(ride.leftChild, rideNumberFrom, rideNumberTo, rideDetails)
            if rideNumberFrom <= ride.rideNumber and rideNumberTo >= ride.rideNumber:
                info = '('+str(ride.rideNumber)+','+str(ride.rideCost)+','+str(ride.tripDuration)+')'
                rideDetails.append(info)
            if rideNumberTo > ride.rideNumber:
                self.print_ride_helper(ride.rightChild, rideNumberFrom, rideNumberTo, rideDetails)


        #cancel ride from red black tree and min heap in the cancel(rideNumber) operation
        def cancel_ride(self, rideNumber):
            if rideNumber in ridePointers:
                self.cancel_ride_helper(self.root, rideNumber)
                self.minheapInstance.cancelRide(ridePointers[rideNumber]) 

        #removes a ride from the red black tree
        def remove_ride(self, rideNumber):
                self.cancel_ride_helper(self.root, rideNumber)

        #finds the node with rideNumber and deletes it. performs rebalancing
        def cancel_ride_helper(self, ride, rideNumber):
            gpride = self.TNULL
            while ride != self.TNULL:
                if ride.rideNumber == rideNumber:
                    gpride = ride

                if ride.rideNumber <= rideNumber:
                    ride = ride.rightChild
                else:
                    ride = ride.leftChild

            if gpride == self.TNULL:
                print("No active ride requests")
                return

            rideToCancel = gpride
            rideToCancel_original_color = rideToCancel.nodecolor
            if gpride.leftChild == self.TNULL:
                x = gpride.rightChild
                self.rbRebalancing(gpride, gpride.rightChild)
            elif (gpride.rightChild == self.TNULL):
                x = gpride.leftChild
                self.rbRebalancing(gpride, gpride.leftChild)
            else:
                rideToCancel = self.minimum(gpride.rightChild)
                rideToCancel_original_color = rideToCancel.nodecolor
                x = rideToCancel.rightChild
                if rideToCancel.parentRide == gpride:
                    x.parentRide = rideToCancel
                else:
                    self.rbRebalancing(rideToCancel, rideToCancel.rightChild)
                    rideToCancel.rightChild = gpride.rightChild
                    rideToCancel.rightChild.parentRide = rideToCancel

                self.rbRebalancing(gpride, rideToCancel)
                rideToCancel.leftChild = gpride.leftChild
                rideToCancel.leftChild.parentRide = rideToCancel
                rideToCancel.nodecolor = gpride.nodecolor
            if rideToCancel_original_color == 'B':
                self.rotationAndRecoloring_deleteRBT(x)

        def rbRebalancing(self, x, y):
            if x.parentRide == None:
                self.root = y
            elif x == x.parentRide.leftChild:
                x.parentRide.leftChild = y
            else:
                x.parentRide.rightChild = y
            y.parentRide = x.parentRide

        #rotates and recolors after performing deletion
        def rotationAndRecoloring_deleteRBT(self, ride):
            while ride != self.root and ride.nodecolor == 'B':
                if ride == ride.parentRide.leftChild:
                    childride = ride.parentRide.rightChild
                    if childride.nodecolor == 'R':
                        childride.nodecolor = 'B'
                        ride.parentRide.nodecolor = 'R'
                        self.l_rotation(ride.parentRide)
                        childride = ride.parentRide.rightChild

                    if childride.leftChild.nodecolor == 'B' and childride.rightChild.nodecolor == 'B':
                        childride.nodecolor = 'R'
                        ride = ride.parentRide
                    else:
                        if childride.rightChild.nodecolor == 'B':
                            childride.leftChild.nodecolor = 'B'
                            childride.nodecolor = 'R'
                            self.r_rotation(childride)
                            childride = ride.parentRide.rightChild

                        childride.nodecolor = ride.parentRide.nodecolor
                        ride.parentRide.nodecolor = 'B'
                        childride.rightChild.nodecolor = 'B'
                        self.l_rotation(ride.parentRide)
                        ride = self.root
                else:
                    childride = ride.parentRide.leftChild
                    if childride.nodecolor == 'R':
                        childride.nodecolor = 'B'
                        ride.parentRide.nodecolor = 'R'
                        self.r_rotation(ride.parentRide)
                        childride = ride.parentRide.leftChild

                    if childride.rightChild.nodecolor == 'B' and childride.rightChild.nodecolor == 'B':
                        childride.nodecolor = 'R'
                        ride = ride.parentRide
                    else:
                        if childride.leftChild.nodecolor == 'B':
                            childride.rightChild.nodecolor = 'B'
                            childride.nodecolor = 'R'
                            self.l_rotation(childride)
                            childride = ride.parentRide.leftChild

                        childride.nodecolor = ride.parentRide.nodecolor
                        ride.parentRide.nodecolor = 'B'
                        childride.leftChild.nodecolor = 'B'
                        self.r_rotation(ride.parentRide)
                        ride = self.root
            ride.nodecolor = 'B'

        #returns the left child ride of the ride passed in the arguments
        def minimum(self, ride):
            while ride.leftChild != self.TNULL:
                ride = ride.leftChild
            return ride

        #performs updatation on the ride with rideNumber in both red black and min heap
        def updateTrip(self, rideNumber, newTripDuration):
            self.update_ride_helper(self.root, rideNumber, newTripDuration)
            self.minheapInstance.updateTrip(ridePointers[rideNumber],newTripDuration)

        #updation in red black tree ride based on the newTripDuration
        def update_ride_helper(self, ride, rideNumber, newTripDuration):
            if rideNumber == ride.rideNumber:
                if newTripDuration <= ride.tripDuration:
                    ride.tripDuration = newTripDuration
                elif ride.tripDuration < newTripDuration and newTripDuration<=2*ride.tripDuration:
                    ride.rideCost = ride.rideCost+10
                    ride.tripDuration = newTripDuration
                elif newTripDuration> 2*ride.tripDuration:
                    self.cancel_ride_helper(self.root, rideNumber)
                return
            elif ride == self.TNULL:
                print('No active ride requests')
                return

            if rideNumber < ride.rideNumber:
                return self.update_ride_helper(ride.leftChild, rideNumber, newTripDuration)
            return self.update_ride_helper(ride.rightChild, rideNumber, newTripDuration)

        #removes the ride from the red black tree with the rideNumber of the root node of min heap
        def getNextRide(self,):
            nextRide = self.minheapInstance.getNextRide()
            if nextRide:
                self.remove_ride(nextRide[0])
                print('('+str(nextRide[0])+','+str(nextRide[1])+','+str(nextRide[2])+')', file=f)
            else:
                print('No active ride requests', file=f)

    if __name__ == "__main__":

        if len(sys.argv) < 2:
            print("Usage: python3 gatorTaxi.py input_file.txt")
            sys.exit(1)
        #min head initialization with max size as 100
        mheap = MinHeap(100)
        #red black tree initialization
        rbt = RedBlackTree(mheap)
        #reads filename from command line args
        filename = sys.argv[1]
        #opens the file to read input data
        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                operation, args = line.strip().split('(')
                args = re.findall('\d+', args)
                if operation == 'Insert':
                    ride_number, ride_cost, trip_duration = map(int, args)
                    rbt.insertRBT(ride_number,ride_cost,trip_duration)
                    mheap.insertMHeap(ride_number,ride_cost,trip_duration)
                elif operation == 'Print':
                    if len(args) == 1:
                        ride_number = int(args[0])
                        rbt.print_ride(ride_number)
                    elif len(args) == 2:
                        ride_number1, ride_number2 = map(int, args)
                        rbt.print_ride(ride_number1, ride_number2)
                elif operation == 'UpdateTrip':
                    ride_number, new_trip_duration = map(int, args)
                    rbt.updateTrip(ride_number, new_trip_duration)
                elif operation == 'GetNextRide':
                    rbt.getNextRide()
                elif operation == 'CancelRide':
                    ride_number = int(args[0])
                    rbt.cancel_ride(ride_number)

                line = file.readline()
        
        file.close()
        f.close()