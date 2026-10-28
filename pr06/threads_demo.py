
import threading
import time

COUNTER_LIMIT = 100_000
THREADS_COUNT = 4

counter = 0
lock = threading.Lock()


def increment(use_lock):
    global counter

    for _ in range(COUNTER_LIMIT):
        if use_lock:
            with lock:
                counter += 1
        else:
            counter += 1


def run_test(use_lock):
    global counter
    counter = 0

    threads = [
        threading.Thread(target=increment, args=(use_lock,))
        for _ in range(THREADS_COUNT)
    ]

    start = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start

    print(f"Lock: {use_lock}")
    print(f"Counter: {counter}")
    print(f"Time: {elapsed:.4f} seconds")

    if use_lock:
        assert counter == 400_000
        print("Correct result: 400000")

    print()


if __name__ == "__main__":
    run_test(False)
    run_test(True)
