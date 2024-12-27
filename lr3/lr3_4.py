import threading
import time
import platform

counter = 0
counter_lock = threading.RLock()

num_iterations = 100000

def increment_counter():
    global counter
    for _ in range(num_iterations):
        counter_lock.acquire()
        try:
            value = counter
            value += 1
            counter = value
        finally:
            counter_lock.release()

def decrement_counter():
    global counter
    for _ in range(num_iterations):
        counter_lock.acquire()
        try:
            value = counter
            value -= 1
            counter = value
        finally:
            counter_lock.release()

def main(n, m):
    global counter
    counter = 0
    increment_threads = [threading.Thread(target=increment_counter) for _ in range(n)]
    decrement_threads = [threading.Thread(target=decrement_counter) for _ in range(m)]

    start_time = time.time()
    for thread in increment_threads + decrement_threads:
        thread.start()

    for thread in increment_threads + decrement_threads:
        thread.join()

    end_time = time.time()

    execution_time = (end_time - start_time) * 1000

    return counter, execution_time

def save_results_to_file(filename, results):
    with open(filename, 'w') as f:
        f.write("Number of Threads | Counter Value | Execution Time (ms)\n")
        f.write("-" * 50 + "\n")
        for result in results:
            f.write(f"{result['threads']:>16} | {result['counter']:>13} | {result['time']:>18.2f}\n")
        f.write("\nSystem Specifications:\n")
        f.write(f"Processor: {platform.processor()}\n")
        f.write(f"Memory: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n")
        f.write(f"OS: {platform.system()} {platform.release()}\n")


if __name__ == "__main__":
    import psutil
    results = []
    thread_counts = [1, 2, 4, 8]
    for count in thread_counts:
        counter_value, exec_time = main(count, count)
        results.append(
            {'threads': count, 'counter': counter_value, 'time': exec_time})

    save_results_to_file("lr3.txt", results)