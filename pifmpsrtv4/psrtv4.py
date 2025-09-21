import time
import threading
import os

RDS_CTL = "rds_ctl"   # FIFO, который создаёт pi_fm_rds

ps_file = "ps.txt"
rt_file = "rt.txt"

f = None
lock = threading.Lock()

# ---------- ВСПОМОГАТЕЛЬНОЕ ----------

def align_ps(seg: str, align: str) -> str:
    """Выравнивание куска seg внутри 8-символьного PS."""
    if len(seg) > 8:
        seg = seg[:8]
    pad = 8 - len(seg)
    if align == "r":
        return " " * pad + seg
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + seg + " " * right
    # l (по умолчанию)
    return seg + " " * pad

def parse_ps_line(raw_line: str):
    """
    Парсит строку из ps.txt в структуру:
    kind: "normal" | "scroll" | "transfer"
    align: 'l' | 'c' | 'r'
    n: длина кадра для transfer (8/6/4)
    text: исходный текст (включая пробелы и | внутри)
    delay: задержка на кадр (сек)
    """
    line = raw_line.rstrip("\n")
    if not line or line.lstrip().startswith("#"):
        return None

    # Выделяем задержку: берём ЧИСЛО после последней |
    delay = 5
    core = line
    pos_last = line.rfind("|")
    if pos_last != -1:
        tail = line[pos_last + 1:]
        try:
            delay = int(tail.strip())
            core = line[:pos_last]
        except ValueError:
            core = line  # нет валидной задержки — оставляем по умолчанию

    # Теперь core может быть "mode|TEXT" или просто "TEXT"
    mode_token = ""
    text = core
    first_bar = core.find("|")
    if first_bar != -1:
        mode_token = core[:first_bar]
        text = core[first_bar + 1:]

    # Значения по умолчанию
    kind = "normal"
    align = "l"
    n = 8

    mt = mode_token

    if mt == "s":  # скролл (без авто-пробелов)
        kind = "scroll"

    else:
        # Варианты: l| / c| / r|  (обычный)
        #           t / t6 / t4   (перенос слева)
        #           lt / lt6 / lt4; ct*; rt* (перенос с выравниванием)
        if mt.startswith(("l", "c", "r")):
            align = mt[0]
            rest = mt[1:]
            if rest == "" or rest is None:
                kind = "normal"
            elif rest.startswith("t"):
                kind = "transfer"
                # длина сегмента (t/t8/t6/t4)
                if len(rest) == 1:
                    n = 8
                else:
                    try:
                        n = int(rest[1:])
                    except ValueError:
                        n = 8
            else:
                kind = "normal"  # неизвестный постфикс — считаем обычным

        elif mt.startswith("t"):  # перенос слева по умолчанию
            kind = "transfer"
            if len(mt) == 1:
                n = 8
            else:
                try:
                    n = int(mt[1:])
                except ValueError:
                    n = 8
            align = "l"

        elif mt == "":  # просто текст
            kind = "normal"
            align = "l"

        else:
            # Непонятный префикс — считаем, что это часть текста
            kind = "normal"
            align = "l"
            text = core  # вернуть всё как текст

    return {"kind": kind, "align": align, "n": n, "text": text, "delay": delay}

def ps_frames(entry):
    """Итератор кадров (строка PS длиной 8) и их задержек."""
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delay = entry["delay"]

    if kind == "normal":
        yield align_ps(text, align), delay

    elif kind == "scroll":
        # Без авто-пробелов: если текста < 8 — один кадр с доп. пробелами справа
        if len(text) <= 8:
            yield align_ps(text, "l"), delay
        else:
            for i in range(0, len(text) - 7):
                yield text[i:i+8], delay

    elif kind == "transfer":
        # t/t6/t4: по n символов, каждый кусок выравниваем в 8
        if n <= 0:
            n = 8
        for i in range(0, len(text), n):
            seg = text[i:i+n]
            yield align_ps(seg, align), delay

def load_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]

def load_rt_list(filename):
    """RT как раньше: 'ТЕКСТ|СЕК'. Внутренние | в тексте поддерживаются."""
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

def send_cmd(cmd: str):
    with lock:
        f.write(cmd + "\n")
        f.flush()
    print(f"[SEND] {cmd}")

# ---------- ПОТОКИ ----------

def cycle_ps():
    while True:
        lines = load_lines(ps_file)
        if not lines:
            time.sleep(1)
            continue
        for raw in lines:
            parsed = parse_ps_line(raw)
            if not parsed:
                continue
            for frame, d in ps_frames(parsed):
                send_cmd(f"PS {frame}")
                time.sleep(d)

def cycle_rt():
    # RT оставляем «старым» форматом (текст|сек)
    while True:
        rt_list = load_rt_list(rt_file)
        if not rt_list:
            time.sleep(1)
            continue
        for rt, d in rt_list:
            # RT передаём как есть (до 64 символов), дополним справа при необходимости
            txt = (rt[:64]).ljust(64)
            send_cmd(f"RT {txt}")
            time.sleep(d)

# ---------- MAIN ----------

if __name__ == "__main__":
    f = open(RDS_CTL, "w")   # открыть FIFO один раз

    threading.Thread(target=cycle_ps, daemon=True).start()
    threading.Thread(target=cycle_rt, daemon=True).start()

    while True:
        time.sleep(1)
