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
    increment_threads = [threading.Thread(target=increment_counter) for _ in range(n)]
    decrement_threads = [threading.Thread(target=decrement_counter) for _ in range(m)]

    start_time = time.time()
    for thread in increment_threads + decrement_threads:
        thread.start()

    for thread in increment_threads + decrement_threads:
        thread.join()

    end_time = time.time()

    print(f"Final counter value: {counter}")
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main(10, 10)