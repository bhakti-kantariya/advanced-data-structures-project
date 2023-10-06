GatorTaxi is a new application that handles the ride sharing requests and this software is a part
of it. It handles the remaining ride requests one by one which are in the pending queue and
performs operations as requested by the users.  
**Implemented using min-heap and a Red-Black Tree (RBT)**   

**Following are the operations of GatorTaxi:**  
1. Print(rideNumber) prints the triplet (rideNumber, rideCost, tripDuration).
2. Print(rideNumber1, rideNumber2) prints all triplets (rx, rideCost, tripDuration) for which rideNumber1 <= rx <= rideNumber2.
3. Insert (rideNumber, rideCost, tripDuration) where rideNumber differs from existing ride numbers.
4. GetNextRide() When this function is invoked, the ride with the lowest rideCost (ties are broken by selecting the ride with the lowest tripDuration) is output. This ride is then deleted from the data structure.
5. CancelRide(rideNumber) deletes the triplet (rideNumber, rideCost, tripDuration) from the data structures, can be ignored if an entry for rideNumber doesn’t exist.
6. UpdateTrip(rideNumber, new_tripDuration) where the rider wishes to change the destination, in this case,
a) if the new_tripDuration <= existing tripDuration, there would be no action needed.
b) if the existing_tripDuration < new_tripDuration <= 2*(existing tripDuration), the driver will cancel the existing ride and a new ride request would be created with a penalty of 10 on existing rideCost . We update the entry in the data structure with (rideNumber, rideCost+10, new_tripDuration)
c) if the new_tripDuration > 2*(existing tripDuration), the ride would be automatically declined and the ride would be removed from the data structure.

**Steps to run the code:**
1. Change directory to gatorTaxi  
2. run _make_  
or  
run _python3 gatorTaxi.py <input_file.txt>_

The output gets generated in the output_file.txt
