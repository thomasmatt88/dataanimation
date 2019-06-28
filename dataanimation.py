import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas
import tkinter as tk
from tkinter import messagebox

def main():
    root_win = tk.Tk()
    cls_ref = DataAnimationGui(root_win)
    root_win.mainloop()
    
class DataAnimationGui:
    def __init__(self, master):
        self.data_file_path = ""
        self.df = pandas.DataFrame()
        
        # --------------- frames --------------------------------------------------------
        topframe = tk.Frame(master)
        topframe.pack(side = tk.TOP)
        middleframe = tk.Frame(master)
        middleframe.pack(side = tk.TOP)
        middleleftframe = tk.Frame(middleframe)
        middleleftframe.pack(side = tk.LEFT)
        middlemiddleframe = tk.Frame(middleframe)
        middlemiddleframe.pack(side = tk.LEFT)
        middlerightframe = tk.Frame(middleframe)
        middlerightframe.pack(side = tk.LEFT)
        bottomframe = tk.Frame(master)
        bottomframe.pack(side = tk.TOP)
        bottomleftframe = tk.Frame(bottomframe)
        bottomleftframe.pack(side = tk.LEFT)
        bottomrightframe = tk.Frame(bottomframe)
        bottomrightframe.pack(side = tk.LEFT)

        # --------------- buttons -------------------------------------------------------
        self.fileButton = tk.Button(topframe, text = "Open File", \
                                    command = self.fileopen)
        self.fileButton.pack(side = tk.LEFT)
        self.createButton = tk.Button(topframe, text = "Create Animation", \
                                      command = self.create_animation)
        self.createButton.pack(side = tk.LEFT)
        self.quitButton = tk.Button(topframe, text = "Quit", \
                                    command = master.destroy)
        self.quitButton.pack(side = tk.RIGHT)

        # ---------------- labels -------------------------------------------------------
        self.x_axis_label = tk.Label(middleleftframe, text = "X-Axis: ")
        self.x_axis_label.pack(side = tk.LEFT)
        self.y_axis_label = tk.Label(middlemiddleframe, text = "Y-Axis: ")
        self.y_axis_label.pack(side = tk.LEFT)
        self.t_axis_label = tk.Label(middlerightframe, text = "Time-Axis: ")
        self.t_axis_label.pack(side = tk.LEFT)       

        self.x_axis_title_label = tk.Label(bottomleftframe, \
                                           text = "X-Axis Title: ")
        self.x_axis_title_label.pack(side = tk.LEFT)
        self.y_axis_title_label = tk.Label(bottomrightframe, \
                                           text = "Y-Axis Title: ")
        self.y_axis_title_label.pack(side = tk.LEFT)

        # ---------------- entry -------------------------------------------------------
        self.x_axis_title = tk.StringVar()
        self.x_axis_title_entry = tk.Entry(bottomleftframe, \
                                        textvariable = self.x_axis_title)
        self.x_axis_title_entry.pack(side = tk.LEFT)

        self.y_axis_title = tk.StringVar()
        self.y_axis_title_entry = tk.Entry(bottomrightframe, \
                                        textvariable = self.y_axis_title)
        self.y_axis_title_entry.pack(side = tk.LEFT)       
        
        # ---------------- drop down menus ----------------------------------------------
        # X-Axis:
        self.selected_x_axis = tk.StringVar(middleleftframe) #track what x_axis_menu is set to
        self.x_axis_options = [None]
        self.selected_x_axis.set(self.x_axis_options[0])
        self.x_axis_menu = tk.OptionMenu(middleleftframe, self.selected_x_axis, \
                                         *self.x_axis_options)
        self.x_axis_menu.pack(side = tk.LEFT)

        # Y-Axis
        self.selected_y_axis = tk.StringVar(middlemiddleframe) #track what y_axis_menu is set to
        self.y_axis_options = [None]
        self.selected_y_axis.set(self.y_axis_options[0])
        self.y_axis_menu = tk.OptionMenu(middlemiddleframe, self.selected_y_axis, \
                                         *self.y_axis_options)
        self.y_axis_menu.pack(side = tk.LEFT)

        # Time-Axis
        self.selected_t_axis = tk.StringVar(middlerightframe) #track what t_axis_menu is set to
        self.t_axis_options = [None]
        self.selected_t_axis.set(self.t_axis_options[0])
        self.t_axis_menu = tk.OptionMenu(middlerightframe, self.selected_t_axis, \
                                         *self.t_axis_options)
        self.t_axis_menu.pack(side = tk.LEFT)       
        
    # helpers ---------------------------------------------------------------------------
    def fileopen(self):
        "open file and update df and menu options"
        self.data_file_path = tk.filedialog.askopenfile()
        self.df = pandas.read_csv(self.data_file_path)
        self.set_x_axis_options(list(self.df.columns.values))
        self.set_x_axis_menu()
        self.set_y_axis_options(list(self.df.columns.values))
        self.set_y_axis_menu()
        self.set_t_axis_options(list(self.df.columns.values))
        self.set_t_axis_menu()       

    def create_animation(self):
        try:
            # start of gui access ----------------------------------------------------------
            TABLE = self.get_df() # dataframe from file chosen in gui
            usr_x_axis = self.selected_x_axis.get() # x_axis chosen in gui
            usr_y_axis = self.selected_y_axis.get() # y_axis chosen in gui
            usr_x_axis_title = self.x_axis_title.get() # x_axis title from gui
            usr_y_axis_title = self.y_axis_title.get() # y_axis title from gui
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
                                          fargs = (xs, ys, usr_x_axis, usr_x_axis_title,
                                                   usr_y_axis, usr_y_axis_title, fig, ax1, \
                                                   TABLE), repeat = False)

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
        except:
            messagebox.showinfo(message = "Error: Did you choose X-axis " + \
                                " and Y-axis from dropdown menus?")

    # mutators --------------------------------------------------------------------------
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

    def set_selected_t_axis(self, select):
        self.selected_t_axis = select

    def set_t_axis_options(self, user_list):
        self.t_axis_options = user_list
        return True

    def set_t_axis_menu(self):
        self.t_axis_menu["menu"].delete(0, 'end')
        for item in self.t_axis_options:
            self.t_axis_menu["menu"].add_command(label = item, \
                                                 command = lambda v = item: self.selected_t_axis.set(v))

    def set_selected_t_axis(self, select):
        self.selected_t_axis = select
    
    # accessors --------------------------------------------------------------------------
    def get_x_axis_options(self):
        return self.x_axis_options
    
    def get_y_axis_options(self):
        return self.y_axis_options

    def get_df(self):
        return self.df

def data_for_animate(time, x_axis, y_axis, df):
    "returns xs and ys from df as of 'time' to be plotted in 'animate'"
    X_series = df[df.TIME == time][x_axis] # linked to gui
    X_list = X_series.tolist()

    Y_series = df[df.TIME == time][y_axis] # linked to gui
    Y_list = Y_series.tolist()
    
    return X_list, Y_list

def animate(interval, xs, ys, x_axis, x_axis_title, y_axis, y_axis_title, \
            figure, subplot, data_frame):
    """plot data from data_frame on subplot as of time = 'interval'
       xs = []
       ys = []
       x_axis, y_axis are column headers of data_frame that animate
                      will plot against each other 
    """

    time = interval #interval is number of times 'animate' has been called
                    #by FuncAnimation

    if time in data_frame.TIME.unique(): # if 'time' is a datapoint in df then plot data
        X, Y = data_for_animate(time, x_axis, y_axis, data_frame)
        xs.extend(X) #extend list X to end of list xs
        ys.extend(Y)
        subplot.clear() # clear the subplot
        subplot.scatter(xs, ys)
        subplot.set_xlabel(x_axis_title, fontweight = 'bold')
        subplot.set_ylabel(y_axis_title, fontweight = 'bold')
        # DataFrame.items() returns zip object. Convert to list, access [0][1],
        # then convert to string
        subplot.set_title(str(list(data_frame[data_frame.TIME == time].TIME.items())[0][1]) \
                          + 's', fontweight = 'bold')
    # save figure EVERY time animate() is called
    figure.savefig('Output_Images/' + str(time) + '.png')
    return

if __name__ == "__main__":
    main()
