import os
import time


pid = os.fork()

if pid == 0:
    print(f"Ребёнок: PID={os.getpid()}, PPID={os.getppid()}")

    time.sleep(5)

    print(
        f"После завершения родителя: "
        f"PID={os.getpid()}, PPID={os.getppid()}"
    )

    time.sleep(10)

else:
    print(f"Родитель: PID={os.getpid()}")
    print("Родитель завершается")

    os._exit(0)
