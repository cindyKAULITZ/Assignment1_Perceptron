import matplotlib.pyplot as plt
import numpy as np
#read file
### testing successed expect 2Circles2.txt ###
f = open('2ring.txt','r')
param = f.read()
arr = [e[0:] for e in param.split('\n')]
data = [' '] * len(arr)
print(arr)
for i in range(0,len(arr)):
    temp = [e[0:] for e in arr[i].split(' ')]
    data[i] = [' '] * len(temp)
    for j in range(0,len(temp)):
        if j == (len(temp)-1):
            data[i][j] = int(temp[j])
        else:
            data[i][j] = float(temp[j])
#print(data)

#learning function
learn = 0.8
thr = (-1.0)
w = [-1.0, 0.0, 1.0]
n = 0
y = -1
stop = 0
precise = 5
while stop < len(data) :
    #print(data[n%4][2])
    sgn = round((w[0]*thr) + (w[1]*data[n%4][0]) + (w[2]*data[n%4][1]),precise)
    print('sgn = ',sgn)
    if sgn > 0:
        y = 2 
        print('y=1')
    else:
        y = 1
        print('y=0')

    if y > data[n%4][2]:
        print('y>')
        w[0] = round(w[0] - (learn*thr),precise)
        w[1] = round(w[1] - (learn*data[n%4][0]),precise)
        w[2] = round(w[2] - (learn*data[n%4][1]),precise)
        stop = 0
    elif y < data[n%4][2]:
        print('y<')
        w[0] = round(w[0] + (learn*thr),precise)
        w[1] = round(w[1] + (learn*data[n%4][0]),precise)
        w[2] = round(w[2] + (learn*data[n%4][1]),precise)
        stop = 0 
    else:
        print('y=')
        stop+=1
    n+=1
    print(*w,sep="\n")

    
# make plot

# X = np.random.normal(0, 1, 30) # 每一个点的X值
# Y = np.random.normal(0, 1, 30) # 每一个点的Y值
# T = np.arctan2(Y,X) # for color value

# plt.scatter(X, Y, s=75, c=T, alpha=.5)
# plt.xlim(-1.5, 1.5)
# plt.ylim(-1.5, 1.5)


#plt.show()