import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


# make plot
def remove(target):
    ax.lines.remove(target[0])

def makeLine():
    x1 = np.linspace(xr.min(),xr.max(),1000) # 100 linearly spaced numbers
    x2 = ((-w[1])/w[2])*x1 + (w[0]/w[2])
    
    lines = ax.plot(x1,x2,c = 'indigo')
    plt.pause(0.01)
    remove(lines)
    #fig.canvas.draw()
    
    #ax = fig.add_subplot(111,aspect='equal')

#read file
### testing successed expect 2Circles2.txt ###

f = open('2cring.txt','r')
param = f.read()

arr = [e[0:] for e in param.split('\n')]
data = [' '] * len(arr)
output = [' ']*len(arr)
x_range = [' ']*len(arr)
y_range = [' ']*len(arr)
#print(arr)
for i in range(0,len(arr)):
    temp = [e[0:] for e in arr[i].split(' ')]
    data[i] = [' '] * len(temp)
    for j in range(0,len(temp)):
        if j == (len(temp)-1):
            data[i][j] = int(temp[j])
            output[i] = int(temp[j])
        else:
            data[i][j] = float(temp[j])
            x_range[i] = float(temp[0])
            y_range[i] = float(temp[1])

c = np.unique(output)
xr = np.unique(x_range)
yr = np.unique(y_range)

fig = plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.set_xlim(xr.min() - 0.5, xr.max() + 0.5, auto = False)
ax.set_ylim(yr.min() - 0.5, yr.max() + 0.5, auto = False)
 
T = ('royalblue', 'salmon', 'turquoise') # for color value
cmap = ListedColormap(T[:3])
for index in range(0,len(data)):
    plt.scatter(x = data[index][0], y = data[index][1], s=30, c=cmap(data[index][2]), alpha=1)
#fig.canvas.draw()
plt.ion()


#learning function
learn = 0.9
thr = (-1.0)
w = [-1.0, 0.0, 1.0]
n = 0
y = -1
stop = 0
precise = 5
while (stop < len(data)) & (n < 10000) :
    #print(data[n%4][2])
    sgn = round((w[0]*thr) + (w[1]*data[n%len(data)][0]) + (w[2]*data[n%len(data)][1]),precise)
    print('sgn = ',sgn)
    if sgn > 0:
        y = c.max() 
        print('y=1')
    else:
        y = c.min()
        print('y=0')

    if y > data[n%len(data)][2]:
        print('y>')
        w[0] = round(w[0] - (learn*thr),precise)
        w[1] = round(w[1] - (learn*data[n%len(data)][0]),precise)
        w[2] = round(w[2] - (learn*data[n%len(data)][1]),precise)
        stop = 0
    elif y < data[n%len(data)][2]:
        print('y<')
        w[0] = round(w[0] + (learn*thr),precise)
        w[1] = round(w[1] + (learn*data[n%len(data)][0]),precise)
        w[2] = round(w[2] + (learn*data[n%len(data)][1]),precise)
        stop = 0 
    else:
        print('y=')
        stop+=1
    if n <= 100:
        makeLine()
    elif n%100 == 0 and n > 100 :
        makeLine()
    n+=1
    print(*w,sep="\n")
    print('n = ',n)

plt.ioff()
plt.show()
