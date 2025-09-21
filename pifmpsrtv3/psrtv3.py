import time
import threading
import os

RDS_CTL = "rds_ctl"  # FIFO

ps_file = "ps.txt"
rt_file = "rt.txt"

f = None
lock = threading.Lock()

def load_list(filename):
    """Читает список (текст, задержка) из файла"""
    if not os.path.exists(filename):
        return []
    items = []
    with open(filename, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            if "|" in line:
                text, delay = line.split("|", 1)
                try:
                    delay = int(delay.strip())
                except ValueError:
                    delay = 5
            else:
                text, delay = line, 5
            items.append((text, delay))
    return items

def format_ps(text):
    return text[:8].ljust(8)

def format_rt(text):
    return text[:64].ljust(64)

def send_cmd(cmd: str):
    with lock:
        f.write(cmd + "\n")
        f.flush()
    print(f"[SEND] {cmd}")

def cycle_ps():
    while True:
        ps_list = load_list(ps_file)
        if not ps_list:
            time.sleep(1)
            continue
        for ps, delay in ps_list:
            send_cmd(f"PS {format_ps(ps)}")
            time.sleep(delay)

def cycle_rt():
    while True:
        rt_list = load_list(rt_file)
        if not rt_list:
            time.sleep(1)
            continue
        for rt, delay in rt_list:
            send_cmd(f"RT {format_rt(rt)}")
            time.sleep(delay)

if __name__ == "__main__":
    f = open(RDS_CTL, "w")
    threading.Thread(target=cycle_ps, daemon=True).start()
    threading.Thread(target=cycle_rt, daemon=True).start()
    while True:
        time.sleep(1)
