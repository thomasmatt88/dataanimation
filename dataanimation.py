import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas
import tkinter as tk


class DataAnimationGui:
    def __init__(self, master):
        self.data_file_path = "Data.csv"
        
        # --------------- frames --------------------------------------------------------
        topframe = tk.Frame(master)
        topframe.pack(side = tk.TOP)
        bottomframe = tk.Frame(master)
        bottomframe.pack(side = tk.BOTTOM)
        bottomleftframe = tk.Frame(bottomframe)
        bottomleftframe.pack(side = tk.LEFT)
        bottommiddleframe = tk.Frame(bottomframe)
        bottommiddleframe.pack(side = tk.LEFT)

        # --------------- buttons -------------------------------------------------------
        self.quitButton = tk.Button(topframe, text = "Quit", \
                                    command = topframe.quit)
        self.quitButton.pack(side = tk.RIGHT)
        self.fileButton = tk.Button(topframe, text = "Open File", \
                                    command = self.fileopen)
        self.fileButton.pack(side = tk.LEFT)

        # ---------------- labels --------------------------------------------------------
        self.x_axis_label = tk.Label(bottomleftframe, text = "X-Axis: ")
        self.x_axis_label.pack(side = tk.LEFT)
        self.y_axis_label = tk.Label(bottommiddleframe, text = "Y-Axis: ")
        self.y_axis_label.pack(side = tk.LEFT)

        # ---------------- drop down menus ----------------------------------------------
        # X-Axis:
        self.selected_x_axis = tk.StringVar(bottomleftframe) #track what x_axis_menu is set to
        self.x_axis_options = [None]
        self.selected_x_axis.set(self.x_axis_options[0])
        self.x_axis_menu = tk.OptionMenu(bottomleftframe, self.selected_x_axis, \
                                         *self.x_axis_options)
        self.x_axis_menu.pack(side = tk.LEFT)

        # Y-Axis
        self.selected_y_axis = tk.StringVar(bottommiddleframe) #track what y_axis_menu is set to
        self.y_axis_options = [None]
        self.selected_y_axis.set(self.y_axis_options[0])
        self.y_axis_menu = tk.OptionMenu(bottommiddleframe, self.selected_y_axis, \
                                         *self.y_axis_options)
        self.y_axis_menu.pack(side = tk.LEFT)
        

    def fileopen(self):
        self.data_file_path = tk.filedialog.askopenfile()

    # mutators ---------------------------------------------------------------------------
    def set_x_axis_options(self, user_list):
        self.x_axis_options = user_list
        return True

    def set_x_axis_menu(self):
        self.x_axis_menu["menu"].delete(0, 'end')
        for item in self.x_axis_options:
            self.x_axis_menu["menu"].add_command(label = item, \
                                                 command = lambda v = item: self.selected_x_axis.set(v))

    def set_selected_x_axis(self, select):
        self.selected_x_axis = select

    def set_y_axis_options(self, user_list):
        self.y_axis_options = user_list
        return True

    def set_y_axis_menu(self):
        self.y_axis_menu["menu"].delete(0, 'end')
        for item in self.y_axis_options:
            self.y_axis_menu["menu"].add_command(label = item, \
                                                 command = lambda v = item: self.selected_y_axis.set(v))

    def set_selected_y_axis(self, select):
        self.selected_y_axis = select


    # accessors --------------------------------------------------------------------------
    def get_x_axis_options(self):
        return self.x_axis_options
    
    def get_y_axis_options(self):
        return self.y_axis_options

root_win = tk.Tk()
cls_ref = DataAnimationGui(root_win)
data_file_path = cls_ref.data_file_path
TABLE = pandas.read_csv(data_file_path)
cls_ref.set_x_axis_options(list(TABLE.columns.values))
cls_ref.set_x_axis_menu()
cls_ref.set_y_axis_options(list(TABLE.columns.values))
cls_ref.set_y_axis_menu()
# convert to TIME series to int for handling purposes
TABLE.TIME = TABLE.TIME.astype(int)
root_win.mainloop()



# Set up the empty figure and subplot we want to animate on
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

xs=[]
ys=[]
def data_for_animate(time):
    "returns xs and ys as of 'time' to be plotted in 'animate'"
    POSIT_series = TABLE[TABLE.TIME == time].POSIT
    #POSIT_series = TABLE[TABLE.TIME == time][cls_ref.selected_x_axis.get()] #linked to gui
    POSIT_list = POSIT_series.tolist()
    x = POSIT_list[0]

    #FORCE_series = TABLE[TABLE.TIME == time][cls_ref.selected_y_axis.get()] #linked to gui
    FORCE_series = TABLE[TABLE.TIME == time].FORCE
    FORCE_list = FORCE_series.tolist()
    y = FORCE_list[0]

    xs.append(x)
    ys.append(y)
    return xs, ys

def animate(interval):
    "plot data from TABLE on ax1 as of time = 'interval'"

    time = interval #interval is number of times 'animate' has been called
                    #by FuncAnimation

    if time in TABLE.TIME.unique(): 
        XS, YS = data_for_animate(time)
        ax1.clear() # clear the subplot
        ax1.plot(XS, YS)
        ax1.set_xlabel('Crosshead Displacement (in)', fontweight = 'bold')
        ax1.set_ylabel('Force (lbs)', fontweight = 'bold')
        #https://stackoverflow.com/questions/30787901/how-to-get-a-value-from-a-pandas-dataframe-and-not-the-index-and-object-type
        ax1.set_title(str(TABLE[TABLE.TIME == time].TIME.item()) + 's', \
                      fontweight = 'bold')
        fig.savefig('Output_Images/' + \
                    str(TABLE[TABLE.TIME == time].TIME.item()) + '.png')
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
                              repeat = False)
plt.show()

#all rc settings are stored in a dictionary-like variable called
#matplotlib.rcParams, which is global to the matplotlib package
try:
    plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
    writer = animation.FFMpegWriter(fps = 1) #frame rate for movie = 1 frame/sec
    ani.save('dataanimation.mp4', writer = writer) #specify MovieWriter = writer
except:
    plt.show() #must have plt.show() for fig.savefig() to work in animat()
#ani.save('basic_animation.html', fps = 1, extra_args = ['-vcodec', 'libx264'])
