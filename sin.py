#!/bin/python3

import requests, time, struct, sys
from math import sin, cos, sqrt, pow

url = '' # e.g.: http://192.168.0.42/

fbuf = '' # do not change
xres = 16
yres = 115

def stripes(x,y,ms,coarseness=12):
  color = sin(
        (10*(((x-4)/coarseness)*sin(ms/500) +
        (0.2*(y-4)/coarseness)*cos(ms/300))) +
        ms/1000)
  return color

def dist(x1,y1,x2=xres/2,y2=yres/2):
  return sqrt(pow(x2-x1,2)+pow(y2-y1,2))

def waves(x,y,ms,coarseness=0.15):
  color = sin((dist(x,y,0,0)*((sin(ms/300)+2)*coarseness))+sin(ms/300)*8)
  return color

def waves_moving(x,y,ms,coarseness=0.15):
  cx = (sin(ms/330)+1)*xres/3
  cy = (cos(ms/540)+1)*yres/3
  color = sin((dist(x,y,cx,cy)*((sin(ms/300)+2)*coarseness))+sin(ms/300)*8)
  return color

def setup():
  print(requests.post(url + 'rendering/mode', data=bytes('1', 'utf-8')))

  with open('timings.txt', 'rb') as f:
    print(requests.post(url + 'rendering/timings', data=f.read()))

if __name__ == '__main__':
  setup()

  while True:
    fbuf = ''
    ms = round(time.time() * 100)
    for x in range(0, xres):
      for y in range(0, yres):
        color = waves_moving(x,y,ms) # replace function with waves or stripes if you like
        fbuf += ' ' if color > 0 else 'X'
      fbuf += '\n'
    
    try:
      print(requests.post(url + 'framebuffer', data=bytes(fbuf, 'utf-8')))
    except:
      time.sleep(1)

    time.sleep(0.05)