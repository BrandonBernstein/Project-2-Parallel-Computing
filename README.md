# Project 2 Question 1

## Description of methods: MPI_Bcast(), MPI_Scatter(), and MPI_Allgather(), MP_Alltoall() and MPI_Reduce().

**1. MPI_Bcast**

MPI_Bcast broadcasts a message from one process (the root) to all other processes in a communicator. It takes data from the root and clones it to each processor iteratively, one by one, at each time step.

**2. MPI_Scatter**

MPI_Scatter distributes chunks of an array from the root process to all other processes. Each process receives a unique portion of the array iteratively on each time step with order maintained.

**3. MPI_Allgather**

MPI_Allgather is a collective operation where each process sends its data to all other processors. Similarly, all processors receive data from all other processors. That is, at each time step, each processor sends its data to the next other processor iteratively while simultaneously receiving data at each time step.

**4. MPI_Alltoall**

MPI_Alltoall is an operation where each process sends a unique piece of data to every other process, and receives data from every other process. This can be done n to n or in pairs. Root will send and receive data from itself to processor two, then with three, etc. After processor two receives and sends data with root, it will do the same with processor 4 as the offset is one. This continues iteratively with all processors.

**5: MPI_Reduce**

MPI_Reduce collects data from all processes and combines it using a reduction operation (e.g., sum, max) at the root process. Each processor besides the root sends data with a send buffer to the root, and the root receives that data with a receive buffer.

## Part 2: Implementation of a simple reduce function of column minimums across processors.

While it is easy to get the minimum column-wise for a matrix held on a single processor, a question arises of how to perform this when rows are split among different processors. Additionally, how do we tell which processor has the minimum? To add a little challenge this assignment aims to do so without using the reduce method supplied by MPI. 

This approach distributes the ith row to the ith processor from root using the send and recv methods. This way each processor has its corresponding row of the matrix in order. As previously said, because it is trivial to get the column min on a single processor we claw back all the data to root to recreate that scenario using the gather function. This protocol works only because order is maintained across methods, therefore the matrix only needs to be reconstructed on the first processor to locate summary statistics. The following pseudo code is applied:

```
initialize empty numpy array

if rank == root: 
  create matrix
  save first row to empty numpy array

  For each processor besides root send the ith row

else:
  receive the array sent by root with empty numpy array

# Use the following function:
function My_global_min_loc(rank, N):

  if rank == root:

    regather the data with the gather method at root.
  
    for column in columns:
      take the min and argmin on each column.
  
if rank == root:
  results[f"A{column}"} = [min, argmin]
```

Using the main.py script you can see a small example output (N=5, P=5) in the corresponding log files. Question-1_rank_0.log showcases the initial matrix, when data was sent and gathered, the reconstructed matrix, and the final results. Additionally, Question-1_rank_i.log (i > 0) has the rows each processor received for verification. 

Command used:
```mpirun -n 5 main.py```

When N is considerably large, visualization of steps is impossible, so a showcase of time performance for varying N is displayed below. The script was run for floating numbers on 4 processors at magnitudes 5 through 7 on seawulf. We see that time is stable and increases approximately linearly with N.

| P  | N = 10^5 | N = 10^6 | N = 10^7 |
|----|----------|----------|----------|
| 4  | 0.55822  | 5.75201  | 63.41832 |

 
