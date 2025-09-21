import time
import threading
import os

RDS_CTL = "rds_ctl"   # FIFO, созданный PiFmRds

ps_file = "ps.txt"
rt_file = "rt.txt"

ps_delay = 5
rt_delay = 7

f = None
lock = threading.Lock()

def load_list(filename):
    """Читает список строк из файла"""
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as fh:
        lines = [line.strip() for line in fh if line.strip()]
    return lines

def send_cmd(cmd: str):
    """Отправка команды в rds_ctl"""
    with lock:
        f.write(cmd + "\n")
        f.flush()
    print(f"[SEND] {cmd}")

def cycle_ps():
    while True:
        ps_list = load_list(ps_file)
        if not ps_list:
            time.sleep(ps_delay)
            continue
        for ps in ps_list:
            send_cmd(f"PS {ps}")
            time.sleep(ps_delay)

def cycle_rt():
    while True:
        rt_list = load_list(rt_file)
        if not rt_list:
            time.sleep(rt_delay)
            continue
        for rt in rt_list:
            send_cmd(f"RT {rt}")
            time.sleep(rt_delay)

if __name__ == "__main__":
    f = open(RDS_CTL, "w")   # открываем FIFO один раз

    threading.Thread(target=cycle_ps, daemon=True).start()
    threading.Thread(target=cycle_rt, daemon=True).start()

    while True:
        time.sleep(1)
