
import threading

account_a = 1000
account_b = 1000
lock = threading.Lock()

INITIAL_TOTAL = account_a + account_b
TRANSFER_COUNT = 100_000


def transfer(source, destination, amount):
    global account_a, account_b

    for _ in range(TRANSFER_COUNT):
        with lock:
            if source == "A":
                account_a -= amount
            else:
                account_b -= amount

            if destination == "A":
                account_a += amount
            else:
                account_b += amount


thread1 = threading.Thread(target=transfer, args=("A", "B", 1))
thread2 = threading.Thread(target=transfer, args=("B", "A", 1))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Account A:", account_a)
print("Account B:", account_b)
print("Total:", account_a + account_b)

assert account_a + account_b == INITIAL_TOTAL
print("Total balance is correct!")
