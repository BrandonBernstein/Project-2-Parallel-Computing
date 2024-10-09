import logging
from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
logger_switch = True

N = int(5) # Number of values to be used.

# Setup logger for performance measurements
if rank == 0:
    time_logger = logging.getLogger(f'time_logger')
    time_logger.setLevel(logging.INFO)
    time_file_handler = logging.FileHandler(f'time_logger.log')
    time_file_handler.setLevel(logging.INFO)
    time_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    time_file_handler.setFormatter(time_formatter)
    time_logger.addHandler(time_file_handler)

# Log start time

if logger_switch:
    logger = logging.getLogger(f'advanced_logger_{rank}')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f'Question-1_rank_{rank}.log')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


results = {}
row_data = np.zeros(N)


start_time = MPI.Wtime()

if rank == 0:
    np.set_printoptions(linewidth=np.inf, threshold=np.inf)
    matrix = np.random.rand(size, N)
    row_data = matrix[rank, :]

    if logger_switch:
        logger.info(f"Matrix shape: {matrix.shape}")
        logger.info(f"Matrix:\n{matrix}")

    elif N <= 10:
        print(matrix)

    for i in range(1, size):
        comm.Send(matrix[i, :], dest=i, tag=0)

        if logger_switch:
            logger.info(f"Processor {i} sent row {i+1}")

else:
    comm.Recv(row_data, source=0, tag=0)

    if logger_switch:
            logger.info(f"Processor {rank} received row: {row_data}")

def MY_Global_Min_Loc(size, rank, N):
    gathered_data = comm.gather(row_data, root=0)

    if rank == 0:
        gathered_data = np.array(gathered_data)

        if logger_switch:

            logger.info("Gathered Data:")
            indented_data = "\n" + np.array2string(gathered_data, prefix="    ")
            logger.info(indented_data)

        for column in range(N):
            column_data = gathered_data[:, column]
            min_index = np.argmin(column_data)
            min_value = np.min(column_data)

            results[f"A[{column}]"] = f"For column {column}, processor {min_index} has minimum value {min_value}"

# Call the function to perform minimum lookup
MY_Global_Min_Loc(size, rank, N)

# Print results on the root process
if (rank == 0) & logger_switch:
    for key in results:
            logger.info(results[key])


if rank == 0:
    end_time = MPI.Wtime()
    duration = end_time - start_time
    time_logger.info(f"Values: {N}. Total duration: {duration:.5f} seconds. Processors {size}")



# elif (rank == 0) & (not logger_switch):
#     for key in results:
#         print(results[key])