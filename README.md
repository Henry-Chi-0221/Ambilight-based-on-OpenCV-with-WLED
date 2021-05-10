# Ambilight-based-on-opencv-with-WLED
Read and process frames from usb-video-capture-device ,and transmit output using udp protocol to WLED to control LED strips

# *Notice : This project needs to work with WLED
* WLED github link : https://github.com/Aircoookie/WLED

# Dependencies
* opencv-python
* asyncio
# Usage
* Customize your led layout,default setting is as below
```py
num_leds_left  = 14
num_leds_right = 14
num_leds_top   = 23
num_leds_bottom = 22
```
* Run the code:
```py
python3 capture.py
```
