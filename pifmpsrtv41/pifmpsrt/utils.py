import threading

lock = threading.Lock()

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
    return seg + " " * pad

def send_cmd(fifo, cmd: str):
    """Потокобезопасная отправка команды в FIFO"""
    with lock:
        fifo.write(cmd + "\n")
        fifo.flush()
    print(f"[SEND] {cmd}")
