import os
import time


pid = os.fork()

if pid == 0:
    print(f"Ребёнок: PID={os.getpid()}")
    os._exit(0)

else:
    print(f"Родитель: PID={os.getpid()}")
    print(f"Ребёнок: PID={pid}")
    print("Родитель не вызывает wait() в течение 30 секунд")

    time.sleep(30)
