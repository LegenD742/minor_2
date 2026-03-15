import multiprocessing
import time

def cpu_heavy_task(n):
    """A simple brute-force primality test to keep the CPU busy."""
    count = 0
    for i in range(2, n):
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                break
        else:
            count += 1
    return count

if __name__ == "__main__":
    # Adjust 'num_range' higher if your CPU is a beast
    num_range = 250000 
    cores = multiprocessing.cpu_count()
    
    print(f"Starting heavy load on {cores} cores...")
    start_time = time.time()

    # Create a process for each core
    processes = []
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_heavy_task, args=(num_range,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Done! Total time: {end_time - start_time:.2f} seconds.")