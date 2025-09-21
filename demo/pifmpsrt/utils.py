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

def align_rt(text: str, align: str) -> str:
    """Выравнивание RT (64 символа)."""
    if len(text) > 64:
        text = text[:64]
    pad = 64 - len(text)
    if align == "r":
        return " " * pad + text
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + text + " " * right
    return text + " " * pad

def send_cmd(fifo, cmd: str):
    """Потокобезопасная отправка команды в FIFO"""
    with lock:
        fifo.write(cmd + "\n")
        fifo.flush()
    print(f"[SEND] {cmd}")
