# Project 2 Question 1

## Description of methods: MPI_Bcast(), MPI_Scatter(), and MPI_Allgather(), MP_Alltoall() and MPI_Reduce().

**1. MPI_Bcast**
MPI_Bcast broadcasts a message from one process (the root) to all other processes in a communicator. Taking data from the root and cloning it to each processor iteratively one by one on each time step.

**2. MPI_Scatter**
MPI_Scatter distributes chunks of an array from the root process to all other processes. Each process receives a unique portion of the array iteratively on each time step with order maintained.

**3. MPI_Allgather**
MPI_Allgather is a collective operation where each process sends its data to all other processes, and all processes receive the entire set of data from everyone. That is, at each time step, each processor sends its data to the next other processor iteratively while simultaneously receiving data at each time step.

**4. MPI_Alltoall**
MPI_Alltoall is an operation where each process sends a unique piece of data to every other process, and receives data from every other process. This can be done n to n or in pairs. So root will send and receive data from itself to processor two, then with three, etc. After processor two receives and sends data with root, it will do the same with processor 4 as the offset is one. This continues iteratively with all processors.

**5: MPI_Reduce**
MPI_Reduce collects data from all processes and combines it using a reduction operation (e.g., sum, max) at the root process. Each processor besides the root sends data with a send buffer to the root, and the root receives that data with a receive buffer.

## Part 2: Implementation of a simple reduce function of column minimums across processors.

While it is easy to get the minimum column-wise for a matrix held on a single processor, a question arises of how to perform this when rows are split among different processors. In this case we avoid using the reduce function. This method relies on using the send, recv and gather methods to send the row data to each processor, then claw back that row data in order. This protocol works only because order is maintained across methods, therefore the matrix only needs to be reconstructed on the first processor to locate summary statistics. The following psuedo code is applied:

```
if root: 
  create matrix
  save first row

  For each processor besides root send the ith row

else:
  receive the array sent by root

# Use the following function:
function My_global_min_loc(rank, N):

  if rank == root:

    regather the data with the gather method at root.
  
    for column in columns:
      take the min and argmin on each column. # Can be done because order is maintained.
  
      results[f"A{column}"} = [min, argmin]
```
