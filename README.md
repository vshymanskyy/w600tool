# w600tool
Firmware upload tool for Winner Micro W600 & W601 WiFi

**Works on:** 
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/linux.svg" width="18" height="18" /> Linux,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/windows.svg" width="18" height="18" /> Windows,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/apple.svg" width="18" height="18" /> MacOS

### Features
- Automatically detects bootloader or helps entering `secboot`
- Get/Set MAC address
- Erase image
- Switch to high-speed mode
- Upload `fls`, `img` files

### Usage
```log
usage: w600tool.py [-h] [-p PORT] [--get-mac] [--set-mac SET_MAC] [-e]
                   [-u UPLOAD] [--upload-speed UPLOAD_SPEED]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  --get-mac
  --set-mac SET_MAC
  -e, --erase
  -u UPLOAD, --upload UPLOAD
  --upload-speed UPLOAD_SPEED (default 1000000)
```
