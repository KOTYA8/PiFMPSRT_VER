import os
import time
from .ps_parser import parse_ps_line, ps_frames
from .utils import send_cmd

def cycle_ps(ps_file, fifo):
    ps_entries = []
    ps_mtime = 0
    iterators = []

    while True:
        try:
            mtime = os.path.getmtime(ps_file)
        except FileNotFoundError:
            time.sleep(1)
            continue

        # Если файл изменился — перечитать и добавить новые строки
        if mtime != ps_mtime:
            ps_mtime = mtime
            new_entries = []
            with open(ps_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    entry = parse_ps_line(line)
                    if entry:
                        new_entries.append(entry)
            # Для каждой новой строки создаём итератор кадров
            iterators = [ps_frames(entry) for entry in new_entries]
            ps_entries = new_entries
            print(f"[INFO] Reloaded PS list ({len(ps_entries)} entries)")

        if not iterators:
            time.sleep(1)
            continue

        # Итерация по итераторам по кругу
        for idx, it in enumerate(iterators):
            try:
                frame, delay = next(it)
                send_cmd(fifo, f"PS {frame}")
                time.sleep(delay)
            except StopIteration:
                # когда итератор закончился — создаём новый из текущего entry
                iterators[idx] = ps_frames(ps_entries[idx])
