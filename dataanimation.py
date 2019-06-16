import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas

TABLE = pandas.read_csv("Data.csv")
# convert to TIME series to int for handling purposes
TABLE.TIME = TABLE.TIME.astype(int)

# Set up the empty figure and subplot we want to animate on
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

xs=[]
ys=[]

def animate(interval):

    time = interval #interval is number of times 'animate' has been called
                    #by FuncAnimation

    if time in TABLE.TIME.unique(): 

        POSIT_series = TABLE[TABLE.TIME == time].POSIT
        POSIT_list = POSIT_series.tolist()
        x = POSIT_list[0]

        FORCE_series = TABLE[TABLE.TIME == time].FORCE
        FORCE_list = FORCE_series.tolist()
        y = FORCE_list[0]

        xs.append(x)
        ys.append(y)

        ax1.clear() # clear the subplot
        ax1.plot(xs,ys)
        ax1.set_xlabel('Crosshead Displacement (in)', fontweight = 'bold')
        ax1.set_ylabel('Force (lbs)', fontweight = 'bold')
        #https://stackoverflow.com/questions/30787901/how-to-get-a-value-from-a-pandas-dataframe-and-not-the-index-and-object-type
        ax1.set_title(str(TABLE[TABLE.TIME==time].TIME.item()) + 's', fontweight = 'bold')
    return

#Pass number of frames to 'animate' that is equivalent to max number of seconds
#from Data.csv
#for some reason 0 is called twice so we need to add an extra frame in order
#to get last data point
FRAMES = TABLE.TIME.astype(int).max() + 1

#FuncAnimation will animate to 'fig' based on function passed to it
#called 'animate'. Every 'interval' (1000 ms) 'animate' will be called.
#'interval' is also the delay between 'frames'.
#'repeat' = False because we don't want animation to repeat when the sequence of
#'frames' is completed. 
ani = animation.FuncAnimation(fig, animate, interval = 1000, frames = FRAMES, \
                              repeat=False)

#plt.show()
plt.rcParams['animation.ffmpeg_path']='/usr/local/bin/ffmpeg'
writer = animation.FFMpegWriter(fps=1)
ani.save('dataanimation.mp4', writer=writer)

#ani.save('basic_animation.html', fps = 1, extra_args = ['-vcodec', 'libx264'])
