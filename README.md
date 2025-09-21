# PiFMPSRT_VER
This repository is presented, all versions of [PiFMPSRT](https://github.com/KOTYA8/PiFMPSRT)

`demo` - is test assemblies, may work or not work.

# Installation V1, V2, V3, V4
**1.** In the terminal we write -> `git clone https://github.com/KOTYA8/PiFMPSRT_VER/`  
**2.** Next, select the version a version of PiFMPSRT (psrtv(ver)) and drag to the PiFmRds or PiFMX Directory (psrt.py).  
**3.** Create in the directory PiFmRds or PiFMX -> `mkfifo rds_ctl`  
**4.** In one console we run -> `sudo ./pi_fm_rds -ctl rds_ctl` or `sudo ./pi_fm_x -ctl rds_ctl`  
and in another console we run: `python3 psrtv(ver).py`  
**5.** After the PiFmRds or PiFMX -> `Change ps.txt and rt.txt directory`. Without closing the script, you can change PS and RT by saving a text file.

# Installation V4.1, V5
**1.** In the terminal we write -> `git clone https://github.com/KOTYA8/PiFMPSRT_VER/`  
**2.** Next, select the version a version of PiFMPSRT (psrtv(ver)) and drag to the PiFmRds or PiFMX Directory (psrt.py and pifmpsrt folder).  
**3.** Create in the directory PiFmRds or PiFMX -> `mkfifo rds_ctl`  
**4.** In one console we run -> `sudo ./pi_fm_rds -ctl rds_ctl` or `sudo ./pi_fm_x -ctl rds_ctl`  
and in another console we run: `python3 psrt.py`  
**5.** After the PiFmRds or PiFMX -> pifmpsrt -> `Change ps.txt and rt.txt directory`. Without closing the script, you can change PS and RT by saving a text file. 

# Version
* **V1** - To change only in Python File (psrtv1.py)  
* **V2** - You can in real time change PS and RT in files (ps.txt and rt.txt)  
* **V3** - Support for seconds (PS | Seconds) is added and taken into account the characters (gaps) PS and RT. If seconds are not exhibited, by default, what is written in the script (psrtv3.py) is placed    
* **V4** - Support for transferring text, scrolling by letter, position of the word (left, center, right)  
* **V4.1** - One code is divided into several files for convenience. It is launched through main.py, all files in the pifmpsrt folder (including ps.txt and rt.txt)  
* **V5** - The name main.py on psrt.py. Automatic definition has been added when the ps.txt and rt.txt file is saved. Added support for seconds for transfer and scroll (s/s). Added position support for RT (l, c, r). Support for the readings of 1.2.3.5.7 characters are added.  
