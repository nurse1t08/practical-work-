import os
import subprocess


def get_processes():
    result = subprocess.run(
        ["ps", "-axo", "pid=,ppid=,state=,rss=,comm="],
        capture_output=True,
        text=True
    )

    processes = {}

    for line in result.stdout.splitlines():
        parts = line.split(None, 4)

        if len(parts) < 5:
            continue

        try:
            pid = int(parts[0])
            ppid = int(parts[1])
            state = parts[2]
            rss = parts[3]
            name = parts[4]

            processes[pid] = {
                "pid": pid,
                "ppid": ppid,
                "state": state,
                "rss": rss,
                "name": name
            }

        except ValueError:
            continue

    return processes


processes = get_processes()

current_pid = os.getpid()

result = subprocess.run(
    ["ps", "-p", str(current_pid), "-o", "user="],
    capture_output=True,
    text=True
)

current_user = result.stdout.strip()


user_processes = {}

for pid, info in processes.items():
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "user="],
        capture_output=True,
        text=True
    )

    user = result.stdout.strip()

    if user == current_user:
        user_processes[pid] = info


children = {}

for pid, info in user_processes.items():
    ppid = info["ppid"]

    if ppid not in children:
        children[ppid] = []

    children[ppid].append(pid)


def print_tree(pid, level=0):
    if pid not in user_processes:
        return

    info = user_processes[pid]

    print(
        "  " * level +
        f"PID={info['pid']} "
        f"STATE={info['state']} "
        f"RSS={info['rss']} KB "
        f"{info['name']}"
    )

    for child in sorted(children.get(pid, [])):
        print_tree(child, level + 1)


roots = []

for pid, info in user_processes.items():
    if info["ppid"] not in user_processes:
        roots.append(pid)


print("Дерево процессов текущего пользователя")
print("=" * 60)

for pid in sorted(roots):
    print_tree(pid)
