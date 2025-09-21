import os
from .utils import align_ps

def parse_ps_line(raw_line: str):
    line = raw_line.rstrip("\n")
    if not line or line.lstrip().startswith("#"):
        return None

    delay = 5
    core = line
    pos_last = line.rfind("|")
    if pos_last != -1:
        tail = line[pos_last + 1:]
        try:
            delay = int(tail.strip())
            core = line[:pos_last]
        except ValueError:
            core = line

    mode_token = ""
    text = core
    first_bar = core.find("|")
    if first_bar != -1:
        mode_token = core[:first_bar]
        text = core[first_bar + 1:]

    kind = "normal"
    align = "l"
    n = 8
    mt = mode_token

    if mt == "s":
        kind = "scroll"
    else:
        if mt.startswith(("l", "c", "r")):
            align = mt[0]
            rest = mt[1:]
            if rest == "" or rest is None:
                kind = "normal"
            elif rest.startswith("t"):
                kind = "transfer"
                if len(rest) == 1:
                    n = 8
                else:
                    try:
                        n = int(rest[1:])
                    except ValueError:
                        n = 8
        elif mt.startswith("t"):
            kind = "transfer"
            if len(mt) == 1:
                n = 8
            else:
                try:
                    n = int(mt[1:])
                except ValueError:
                    n = 8
            align = "l"
        elif mt == "":
            kind = "normal"
            align = "l"
        else:
            kind = "normal"
            align = "l"
            text = core

    return {"kind": kind, "align": align, "n": n, "text": text, "delay": delay}

def ps_frames(entry):
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delay = entry["delay"]

    if kind == "normal":
        yield align_ps(text, align), delay
    elif kind == "scroll":
        if len(text) <= 8:
            yield align_ps(text, "l"), delay
        else:
            for i in range(0, len(text) - 7):
                yield text[i:i+8], delay
    elif kind == "transfer":
        if n <= 0:
            n = 8
        for i in range(0, len(text), n):
            seg = text[i:i+n]
            yield align_ps(seg, align), delay

def load_ps_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]
