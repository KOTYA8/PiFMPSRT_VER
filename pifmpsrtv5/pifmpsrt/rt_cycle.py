import os
import time
from .utils import send_cmd, align_rt

def cycle_rt(rt_file, fifo):
    rt_entries = []
    rt_mtime = 0
    iterators = []

    while True:
        try:
            mtime = os.path.getmtime(rt_file)
        except FileNotFoundError:
            time.sleep(1)
            continue

        # Если файл изменился — перечитать и добавить новые строки
        if mtime != rt_mtime:
            rt_mtime = mtime
            new_entries = []
            with open(rt_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.rstrip("\n")
                    if not line or line.lstrip().startswith("#"):
                        continue

                    delay = 5
                    core = line

                    k = line.rfind("|")
                    if k != -1:
                        tail = line[k+1:]
                        try:
                            delay = int(tail.strip())
                            core = line[:k]
                        except ValueError:
                            core = line

                    align = "l"
                    if core.startswith(("l|", "c|", "r|")):
                        align = core[0]
                        core = core[2:]

                    new_entries.append((core, delay, align))

            rt_entries = new_entries
            # создаём итераторы — для RT просто повторение (каждый кадр одно значение)
            iterators = [(rt, delay, align) for rt, delay, align in rt_entries]
            print(f"[INFO] Reloaded RT list ({len(rt_entries)} entries)")

        if not iterators:
            time.sleep(1)
            continue

        for idx, (rt, d, align) in enumerate(iterators):
            txt = align_rt(rt, align)
            send_cmd(fifo, f"RT {txt}")
            time.sleep(d)
