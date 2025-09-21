import time
from .ps_parser import load_ps_lines, parse_ps_line, ps_frames
from .utils import send_cmd

def cycle_ps(ps_file, fifo):
    while True:
        lines = load_ps_lines(ps_file)
        if not lines:
            time.sleep(1)
            continue
        for raw in lines:
            parsed = parse_ps_line(raw)
            if not parsed:
                continue
            for frame, d in ps_frames(parsed):
                send_cmd(fifo, f"PS {frame}")
                time.sleep(d)
