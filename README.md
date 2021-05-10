# Ambilight-based-on-OpenCV-with-WLED
* Read and process frames from usb-video-capture-device ,and transmit output using udp protocol to WLED to control LED strips.
* This project works on Raspberry pi 4.

# Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Sus72gKCD5g/0.jpg)](https://www.youtube.com/watch?v=Sus72gKCD5g)
* https://www.youtube.com/watch?v=Sus72gKCD5g

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
* Adjust resolution

```py
division = 8  #Lower this value may cause lag.
resolution = (1280/division,720/division) 
```
* Run the code:
```py
python3 capture.py
```
