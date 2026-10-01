import os
import time
import subprocess


def get_rss(pid):
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "rss="],
        capture_output=True,
        text=True
    )

    return int(result.stdout.strip())


data = [0] * 10_000_000

print(f"Родитель PID={os.getpid()}")
print(f"Размер списка: {len(data):,} элементов")

pid = os.fork()

if pid == 0:
    child_pid = os.getpid()

    time.sleep(1)

    rss_before = get_rss(child_pid)

    print(f"\nРебёнок PID={child_pid}")
    print(f"RSS до изменения списка: {rss_before} KB")

    for i in range(0, len(data), 100):
        data[i] = 1

    time.sleep(1)

    rss_after = get_rss(child_pid)

    print(f"RSS после изменения списка: {rss_after} KB")
    print(f"Изменение RSS: {rss_after - rss_before} KB")

    os._exit(0)

else:
    os.wait()
    print("\nРодитель: ребёнок завершён")
