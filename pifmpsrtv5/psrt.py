import threading
from pifmpsrt.ps_cycle import cycle_ps
from pifmpsrt.rt_cycle import cycle_rt

RDS_CTL = "rds_ctl"   # FIFO
PS_FILE = "pifmpsrt/ps.txt"
RT_FILE = "pifmpsrt/rt.txt"

if __name__ == "__main__":
    fifo = open(RDS_CTL, "w")

    threading.Thread(target=cycle_ps, args=(PS_FILE, fifo), daemon=True).start()
    threading.Thread(target=cycle_rt, args=(RT_FILE, fifo), daemon=True).start()

    while True:
        try:
            threading.Event().wait(1)
        except KeyboardInterrupt:
            print("Stopping...")
            break
