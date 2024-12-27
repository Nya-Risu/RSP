import threading
import time

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