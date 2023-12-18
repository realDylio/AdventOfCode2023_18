import re
#import pdb
#from IPython.core.debugger import set_trace
#set_trace()
import copy
from collections import defaultdict, Counter
import functools
from math import lcm

import time
import queue

part2 = True
def myprint(arr):
    for a in arr:
        print(a)

def computehex(z):
    
    table = {'0': 0, '1': 1, '2': 2, '3': 3,  
             '4': 4, '5': 5, '6': 6, '7': 7, 
             '8': 8, '9': 9, 'a': 10, 'b': 11,  
             'c': 12, 'd': 13, 'e': 14, 'f': 15} 
  

    res = 0
      
    # computing max power value 
    size = len(z) - 1
      
    for num in z: 
        res = res + table[num]*16**size 
        size = size - 1
        
    return res
    
def readInput(fname):
    
    
    arr = []

    file = open(fname)
    lines = file.readlines()

    data = []

    for line in lines:
        s = []
        line = line.strip()
        if part2:
            tokens = line.split("#")
            full = tokens[1][:-1]
            num = int(full[-1])
            hex = full[:-1]
            d = { 0 : "R", 1 : "D", 2 : "L", 3 : "U"}
        
            data.append([d[num], computehex(hex)])

        else:
            tokens = line.split() 
            data.append([tokens[0], int(tokens[1])])
                      
    return data


        
start_time = time.time()
out = readInput(r"C:\Users\dse\OneDrive\Desktop\input2023\input_18.txt")
myprint(out)

x = 0
y = 0
start = (x,y)
d = dict()
poss = ["R", "L", "U", "D"]
vecs = [(1,0), (-1,0), (0,-1), (0,1)]

for n in range(4):
    d[poss[n]] = vecs[n]
    
ans = 0
corners = []
middles = 0
lastdir = out[-1][0]

pipes = [] #locations of "|" for figuring out interior points using 

for c in out:
    curdir = c[0]
    steps = c[1]
    
    corners.append((x,y, lastdir+curdir))
    middles += steps - 1
    
    
    x1 = x + steps * d[curdir][0]
    y1 = y + steps * d[curdir][1]
    

    delta = 0
    if curdir in [ "D", "U"]:
        delta = (x) * (y1 - y)
    
    if curdir == "D":
        pipes.append([x,y+1,y1-1])
    
    if curdir == "U":
        pipes.append([x,y1+1, y-1])
        
    lastdir = curdir
        
        
    ans += delta
    
    x = x1
    y = y1




def findNumOutside(corners, pipes):
    ans = 0
    for c in corners:
        x = c[0]
        y = c[1]
        
        numpipes = 0
        for p in pipes:
            x1 = p[0]
            y1 = p[1]
            y2 = p[2]
            if x1 < x and y1 <= y <= y2:
                numpipes += 1
                
        ans += findNumForOneSquare(c, corners, numpipes)
        
    return ans

def findNumForOneSquare(c, corners, numpipes):
    x = c[0]
    y = c[1]
    
    ans = 0
    
    if y == 0 and x == 6:
        poo  = 1
    
    #upper left corner
    numpass = 0
    for c in corners:
        x1 = c[0]
        y1 = c[1]
        curd = c[2]
        if y == y1 and x1 < x and (curd[0] == "D" or curd[1] == "U"):
            numpass += 1
             
    if (numpass+numpipes) % 2 == 0:
        ans += 1
        
    #upper right corner
    numpass = 0
    for c in corners:
        x1 = c[0]
        y1 = c[1]
        curd = c[2]
        if y == y1 and x1 <= x and (curd[0] == "D" or curd[1] == "U"):
            numpass += 1
             
    if (numpass+numpipes) % 2 == 0:
        ans += 1
        
    #lower left corner
    numpass = 0
    for c in corners:
        x1 = c[0]
        y1 = c[1]
        curd = c[2]
        if y == y1 and x1 < x and (curd[1] == "D" or curd[0] == "U"):
            numpass += 1
             
    if (numpass+numpipes) % 2 == 0:
        ans += 1
        
    #lower right corner
    numpass = 0
    for c in corners:
        x1 = c[0]
        y1 = c[1]
        curd = c[2]
        if y == y1 and x1 <= x and (curd[1] == "D" or curd[0] == "U"):
            numpass += 1
             
    if (numpass+numpipes) % 2 == 0:
        ans += 1
    
    return ans
        
         
numMissing = findNumOutside(corners, pipes)           

print(ans + .5 * middles +.25 *numMissing)

print("--- %s seconds ---" % (time.time() - start_time)) 
