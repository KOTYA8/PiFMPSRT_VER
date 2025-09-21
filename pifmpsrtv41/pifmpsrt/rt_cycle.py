import os
import time
from .utils import send_cmd

def load_rt_list(filename):
    if not os.path.exists(filename):
        return []
    items = []
    with open(filename, "r", encoding="utf-8") as fh:
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
            items.append((core, delay))
    return items

def cycle_rt(rt_file, fifo):
    while True:
        rt_list = load_rt_list(rt_file)
        if not rt_list:
            time.sleep(1)
            continue
        for rt, d in rt_list:
            txt = rt[:64].ljust(64)
            send_cmd(fifo, f"RT {txt}")
            time.sleep(d)
