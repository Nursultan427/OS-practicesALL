
import threading
import queue
import time

LIMIT = 5
items = queue.Queue(maxsize=LIMIT)
STOP = None


def producer():
    for number in range(10):
        items.put(number)
        print(f"Produced: {number}")
        time.sleep(0.1)

    items.put(STOP)


def consumer():
    while True:
        item = items.get()

        try:
            if item is STOP:
                break

            print(f"Consumed: {item}")
            time.sleep(0.2)
        finally:
            items.task_done()


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

consumer_thread.start()
producer_thread.start()

producer_thread.join()
items.join()
consumer_thread.join()

print("Finished!")
