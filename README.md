<img align="right" height="64" src="/icon.png">

# w600tool
Firmware upload tool for Winner Micro W600 & W601 WiFi

**Works on:** 
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/linux.svg" width="18" height="18" /> Linux,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/windows.svg" width="18" height="18" /> Windows,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/apple.svg" width="18" height="18" /> MacOS

Prebuilt Windows executable file is available [here](https://github.com/vshymanskyy/w600tool/releases/latest)

### Features
- Automatically detects bootloader or helps entering `secboot`
- Get/Set MAC address
- Erase secboot and image
- Switch to high-speed mode
- Upload `fls`, `img` files

### Usage
```log
usage: w600tool.py [-h] [-p PORT] [-b BAUD] [--get-mac] [--set-mac MAC] [-e]
                   [-u FILE]
                   [--upload-baud {115200,460800,921600,1000000,2000000}]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -b BAUD, --baud BAUD
  --get-mac
  --set-mac MAC
  -e, --erase
  -u FILE, --upload FILE
  --upload-baud {115200,460800,921600,1000000,2000000}
```

### Example
```log
$ python3 ./w600tool.py --upload fw/W60X_MicroPython_1.10_B1.1_GZ.img
Push reset button to enter bootloader...
Switched speed to 1000000
Uploading fw/W60X_MicroPython_1.10_B1.1_GZ.img
0% [##############################] 100% | ETA: 00:00:00
Total time elapsed: 00:00:09
Reset board to run user code...
```
