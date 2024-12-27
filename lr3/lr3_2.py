import concurrent.futures
import threading
import time

counter = 0
counter_lock = threading.Lock()

num_iterations = 100000

def increment_counter():
    global counter
    for _ in range(num_iterations):
        with counter_lock:
            value = counter
            value += 1
            counter = value

def decrement_counter():
    global counter
    for _ in range(num_iterations):
        with counter_lock:
            value = counter
            value -= 1
            counter = value


def main(n, m):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n+m) as executor:
        increment_tasks = [executor.submit(increment_counter) for _ in range(n)]
        decrement_tasks = [executor.submit( decrement_counter) for _ in range(m)]

        for task in increment_tasks + decrement_tasks:
            task.result()

    end_time = time.time()

    print(f"Final counter value: {counter}")
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    start_time = time.time()
    main(10, 10)