import os
import time

pid = os.fork()

if pid == 0:
    os._exit(0)
else:
    print(f"PID родителя: {os.getpid()}")
    print(f"PID ребёнка: {pid}")
    print("Родитель ждёт 60 секунд, не вызывая wait()")
    time.sleep(60)
    os.wait()
