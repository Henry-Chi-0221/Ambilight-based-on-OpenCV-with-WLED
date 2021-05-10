import cv2
import numpy as np
import math
import socket
import time
import asyncio
cap = cv2.VideoCapture(0)
division = 8
resolution = (1280/division,720/division)
fps = 5
cap.set(cv2.CAP_PROP_FPS,fps )
cap.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0] )
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1] )

num_leds_left  = 14
num_leds_right = 14
num_leds_top   = 23
num_leds_bottom = 22

width = 20
UDP_IP_ADDRESS = "192.168.1.151"
UDP_PORT_NO = 21324
speed = 0

full_strip = [2,2]

current = np.zeros(221)
current[:2] = 2
current = current.astype(int).tolist()
full_strip = np.zeros(221).astype(int).tolist()

def transmit(current):
    Message = bytearray(current)
    clientSock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto (Message, (UDP_IP_ADDRESS, UDP_PORT_NO))


async def test(x):
    global current
    global full_strip
    while(1):
        diff = full_strip[x]-current[x]
        if(diff>0):
            if(diff<10):
                current[x]+=1
            else:    
                current[x]+=10
        if(diff<0):
            if(diff>-10):
                current[x]-=1
            else:    
                current[x]-=10
            
        await asyncio.sleep(0)

def get_average(src):
    #src = src.copy()
    channels = cv2.mean(src)
    src[:,:] = np.array([(channels[2] , channels[1] , channels[0])])[0]
    return [int(channels[2]) , int(channels[1]) , int(channels[0])]
async def capture():
    while(1):
        ret , frame = cap.read()
        if(ret):
            global full_strip
            left_strip = []
            right_strip = []
            top_strip = []
            bottom_strip = []
            for i in range(num_leds_left):
                #cv2.rectangle(frame ,(0,0),(width,(i+1)*int(resolution[1]/num_leds_left)) , (255,0,0) , 1)
                left_strip.append(get_average(frame[(i)*int(resolution[1]/num_leds_left):(i+1)*int(resolution[1]/num_leds_left),0:width]))
                #print(get_average(frame[(i)*int(resolution[1]/num_leds_left):(i+1)*int(resolution[1]/num_leds_left),0:width]))
                #up to down
            for j in range(num_leds_right):
                #cv2.rectangle(frame ,(resolution[0]-width,0),(resolution[0],(j+1)*int(resolution[1]/num_leds_right)) , (255,0,0) , 1)
                right_strip.append(get_average(frame[(j)*int(resolution[1]/num_leds_right):(j+1)*int(resolution[1]/num_leds_right),-width:]))
                #up to down
            for k in range(num_leds_top):
                #cv2.rectangle(frame ,(0,0),((k+1)*int(resolution[0]/num_leds_top),width) , (255,0,0) , 1)
                top_strip.append(get_average(frame[0:width,(k)*int(resolution[0]/num_leds_top):(k+1)*int(resolution[0]/num_leds_top)]))
                #left to right
            for m in range(num_leds_bottom):
                #cv2.rectangle(frame ,(0,resolution[0]),(m*int(resolution[0] / num_leds_bottom),resolution[1]-width) , (255,0,0) , 1)
                bottom_strip.append(get_average(frame[-width:,(m)*int(resolution[0]/num_leds_bottom):(m+1)*int(resolution[0]/num_leds_bottom)]))
                #left to right
            left_strip = np.array(left_strip)
            right_strip = np.array(right_strip)
            top_strip = np.array(top_strip)
            bottom_strip = np.array(bottom_strip)
        
            full_strip = [2,2]
            for i in range(len(left_strip)):
                i = -i
                full_strip.append(left_strip[i,0])
                full_strip.append(left_strip[i,1])
                full_strip.append(left_strip[i,2])
            for k in range(len(top_strip)):
                full_strip.append(top_strip[k,0])
                full_strip.append(top_strip[k,1])
                full_strip.append(top_strip[k,2])
            for j in range(len(right_strip)):
                full_strip.append(right_strip[j,0])
                full_strip.append(right_strip[j,1])
                full_strip.append(right_strip[j,2])
            for m in range(len(bottom_strip)):
                m=-m
                full_strip.append(bottom_strip[m,0])
                full_strip.append(bottom_strip[m,1])
                full_strip.append(bottom_strip[m,2])
            
            
            
            await asyncio.sleep(0)
            #cv2.imshow('src' , frame)    
            transmit(current)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

async def transmit_async():
    while(1):
        transmit()
        await asyncio.sleep(0)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [test(i) for i in range(221)]
    tasks.append(capture())
    cors = asyncio.wait(tasks)
    loop.run_until_complete(cors)