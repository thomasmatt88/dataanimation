import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas
import tkinter as tk

def main():
    
    # start of gui access ----------------------------------------------------------
    root_win = tk.Tk()
    cls_ref = DataAnimationGui(root_win)
    data_file_path = cls_ref.data_file_path
    TABLE = pandas.read_csv(data_file_path)
    cls_ref.set_x_axis_options(list(TABLE.columns.values))
    cls_ref.set_x_axis_menu()
    cls_ref.set_y_axis_options(list(TABLE.columns.values))
    cls_ref.set_y_axis_menu()
    root_win.mainloop()

    usr_x_axis = cls_ref.selected_x_axis.get() # x_axis chosen in gui
    usr_y_axis = cls_ref.selected_y_axis.get() # y_axis chosen in gui
    # end of gui access ------------------------------------------------------------

    # convert to TIME series to int for handling purposes
    TABLE.TIME = TABLE.TIME.astype(int)
    # Set up the empty figure and subplot we want to animate on
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    
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
    xs = [] # initialized lists to pass to animate()
    ys = []
    ani = animation.FuncAnimation(fig, animate, interval = 1000, frames = FRAMES, \
                                  fargs = (xs, ys, usr_x_axis, usr_y_axis, fig, \
                                           ax1, TABLE), repeat = False)

    #all rc settings are stored in a dictionary-like variable called
    #matplotlib.rcParams, which is global to the matplotlib package
    try:
        plt.show() # plt.show() has to be before ani.save() in order to work
        # must have plt.show() for fig.savefig() to work in animate()
        plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
        writer = animation.FFMpegWriter(fps = 1) #frame rate for movie = 1 frame/sec
        ani.save('dataanimation.mp4', writer = writer) #specify MovieWriter = writer
    except Exception as e:
        print(e)


    
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
                                    command = master.destroy)
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

def data_for_animate(time, x_axis, y_axis, df):
    "returns xs and ys from df as of 'time' to be plotted in 'animate'"
    X_series = df[df.TIME == time][x_axis] # linked to gui
    X_list = X_series.tolist()
    x = X_list[0]

    Y_series = df[df.TIME == time][y_axis] # linked to gui
    Y_list = Y_series.tolist()
    y = Y_list[0]
    
    return x, y

def animate(interval, xs, ys, x_axis, y_axis, figure, subplot, data_frame):
    """plot data from data_frame on subplot as of time = 'interval'
       xs = []
       ys = []
       x_axis, y_axis are column headers of data_frame that animate
                      will plot against each other 
    """

    time = interval #interval is number of times 'animate' has been called
                    #by FuncAnimation

    if time in data_frame.TIME.unique(): 
        X, Y = data_for_animate(time, x_axis, y_axis, data_frame)
        xs.append(X)
        ys.append(Y)
        subplot.clear() # clear the subplot
        subplot.plot(xs, ys)
        subplot.set_xlabel('Crosshead Displacement (in)', fontweight = 'bold')
        subplot.set_ylabel('Force (lbs)', fontweight = 'bold')
        #https://stackoverflow.com/questions/30787901/how-to-get-a-value-from-a-pandas-dataframe-and-not-the-index-and-object-type
        subplot.set_title(str(data_frame[data_frame.TIME == time].TIME.item()) \
                          + 's', fontweight = 'bold')
        figure.savefig('Output_Images/' + \
                    str(data_frame[data_frame.TIME == time].TIME.item()) + '.png')
    return

if __name__ == "__main__":
    main()
