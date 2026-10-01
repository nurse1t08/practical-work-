import os
import sys
import time


if len(sys.argv) < 3:
    print("Использование: python3 runner.py N команда [аргументы]")
    sys.exit(1)


n = int(sys.argv[1])
command = sys.argv[2:]

children = {}


for i in range(n):
    start = time.time()

    pid = os.fork()

    if pid == 0:
        os.execvp(command[0], command)
    else:
        children[pid] = start


for i in range(n):
    pid, status = os.wait()

    end = time.time()
    elapsed = end - children[pid]

    if os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
    else:
        code = -1

    print(
        f"PID={pid} | Код возврата={code} | "
        f"Время работы={elapsed:.3f} сек"
    )
