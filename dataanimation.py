#notes to self:
#interval value passed to def animate is the number of times it has been called by FuncAnimation
#interval value set in FuncAnimation is the delay between frames in ms
#right now set at 10ms
#so every 0.01s def animate is called and the interval value is how many times it has been called

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas

TABLE = pandas.read_csv("Data.csv")

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs=[]
ys=[]

def animate(interval):

    time = interval
    #print(time)
    #convert to TIME series to int for handling purposes
    TABLE.TIME = TABLE.TIME.astype(int)

    if time in TABLE.TIME.unique(): 

        POSIT_series = TABLE[TABLE.TIME == time].POSIT
        POSIT_list = POSIT_series.tolist()
        x = POSIT_list[0]

        FORCE_series = TABLE[TABLE.TIME == time].FORCE
        FORCE_list = FORCE_series.tolist()
        y = FORCE_list[0]

        xs.append(x)
        ys.append(y)

        ax1.clear()
        ax1.plot(xs,ys)
        ax1.set_xlabel('Crosshead Displacement (in)', fontweight = 'bold')
        ax1.set_ylabel('Force (lbs)', fontweight = 'bold')
        #https://stackoverflow.com/questions/30787901/how-to-get-a-value-from-a-pandas-dataframe-and-not-the-index-and-object-type
        ax1.set_title(str(TABLE[TABLE.TIME==time].TIME.item()) + 's', fontweight = 'bold')
    return

#for some reason 0 is called twice so we need to add an extra frame in order to get last data point
FRAMES= TABLE.TIME.astype(int).max()+1   
ani = animation.FuncAnimation(fig, animate, interval=1000, frames=FRAMES, repeat=False)

plt.rcParams['animation.ffmpeg_path']='/usr/local/bin/ffmpeg'
writer = animation.FFMpegWriter(fps=1)
ani.save('dataanimation.mp4', writer=writer)
