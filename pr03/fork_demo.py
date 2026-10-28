import os

pid = os.fork()

if pid == 0:
    print(f"Я ребёнок, PID={os.getpid()}, PPID={os.getppid()}")
    os._exit(0)
else:
    child_pid, status = os.wait()
    print(f"Я родитель, PID={os.getpid()}")
    print(f"Ребёнок {child_pid} завершился с кодом {os.waitstatus_to_exitcode(status)}")
