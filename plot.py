import pylab
import os, json
from time import sleep

# get all of our data files
fileList = map(lambda x: int(x), os.listdir("./data"))
fileList.sort()

# data for each user
data  = {}
mints = False
v = []

# open and read each file
for file in fileList:
    fh = open("./data/" + str(file), "r")
    dl = fh.read()
    
    if len(dl) == 0:
        continue
        
    if mints == False:
        mints = file
    
    try:
        for r in json.loads(dl):
            user  = r[0]
            views = int(r[2])

            if user not in data:
                data[user] = {file : views}
            else:
                data[user][file] = views
                
            v.append(views)
    except ValueError:
        # couldn't parse the file!
        print 'failed on file', file
            
    fh.close()
    maxts = file

# initialise the plot
fig  = pylab.figure(figsize=(15,8))

ax = fig.add_subplot(111)
ax.set_xlabel('time (minutes)')
ax.set_ylabel('viewers')

lines = []
ltext = []
ef = 0

for user in data:
    # dont keep scrubs
    if max(data[user].values()) < 750 or \
       max(data[user].keys())-min(data[user].keys()) < 0.2 * (maxts - mints):
        continue
    
    x = []
    y = []
    lastx = fileList[0] - mints
    
    for i in fileList[1:]:
        rindex = i - mints
        
        if i in data[user]:
            if lastx is False:
                delta = 0
            else:
                # delta
                delta = rindex - lastx

            # if the delta is too big, finish this line
            if delta > 1.1 * (maxts - mints):
                lines.append(ax.plot(x,y, '.'))
                ltext.append(user)
                # we're done
                x = []
                break
            else:
                lastx = rindex
            
            # and now add the points as usual
            xv = float(rindex) / 60
            x.append(xv)
            if xv > ef:
                ef = xv
            y.append(data[user][i])
    
    # still any x left?
    if len(x) > 0:
        lines.append(ax.plot(x,y, '.'))
        ltext.append(user)
    
# set the appropriate x/y ticks
ax.set_yticks(map(lambda x: 2000 * x, range(0,max(v)/2000 + 1)))
ax.set_xticks(range(0, int(ef)+30,30))
fig.legend(lines,ltext)
fig.show()
fig.savefig('graph.png')