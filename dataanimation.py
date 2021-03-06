import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from datafilemeta import creationdate

# custom modules
from videotimestamp import videotimestamp, videoendtime
from videotrim import trim_video
from videotrim import CustomError
from overlayvideo import sync_videos


def main():
    root_win = tk.Tk()
    cls_ref = DataAnimationGui(root_win)
    root_win.mainloop()

class Tab3(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__()
        self.controller = controller
        #self.data_time_stamp = tk.StringVar(value = self.controller.shared_data["test"].get())
        self.data_time_stamp = self.controller.shared_data["data_file_creation"]

        # --------------- frames -----------------------------------------------
        self.topframe = tk.Frame(self) #####
        self.topframe.pack(fill = tk.X, side = tk.TOP)
        #topframe.configure(background = "gray")
        self.middleframe = tk.Frame(self) #####
        self.middleframe.pack(fill = tk.X, side = tk.TOP)

        # --------------- labels -----------------------------------------------
        self.videost_label = tk.Label(self.topframe, text = "Video Start-Time:", fg = "blue")
        self.videost_label.pack(side = tk.LEFT)
        self.videost_choice = tk.Label(self.topframe, \
                                       textvariable = self.controller.shared_data["video_file_start"], \
                                       fg = "blue")
        self.videost_choice.pack(side = tk.LEFT)
        self.videoet_label = tk.Label(self.topframe, text = "Video End-Time:", fg = "blue")
        self.videoet_label.pack(side = tk.LEFT)
        self.videoet_choice = tk.Label(self.topframe, \
                                       textvariable = self.controller.shared_data["video_file_end"], \
                                       fg = "blue")
        self.videoet_choice.pack(side = tk.LEFT)
        
        self.dt_stamp_label = tk.Label(self.middleframe, text = "Data Start-Time: ", fg = "blue")
        self.dt_stamp_label.pack(side = tk.LEFT)

        # --------------- entry -----------------------------------------------
        self.dtime_stamp_entry = tk.Entry(self.middleframe, \
                                        textvariable = self.data_time_stamp)
        self.dtime_stamp_entry.pack(side = tk.LEFT)

        # --------------- labels 2 --------------------------------------------
        self.dataet_label = tk.Label(self.middleframe, text = "Data Duration (s): ", fg = "blue")
        self.dataet_label.pack(side = tk.LEFT)
        self.dataet_choice = tk.Label(self.middleframe, \
                                       textvariable = self.controller.shared_data["data_file_end"], \
                                       fg = "blue")
        self.dataet_choice.pack(side = tk.LEFT)

        # --------------- buttons ---------------------------------------------
        self.syncvideoButton = tk.Button(self.middleframe, text = "Sync Video", \
                                         command = lambda: \
                                         self.sync_helper(self.data_time_stamp.get(), \
                                                          self.controller.shared_data["video_file_start"].get()))
        self.syncvideoButton.pack(side = tk.LEFT)

        # tab3 helper ---------------------------------------------------------
    def sync_helper(self, data_start, video_start):
        try:
            sync_videos(data_start, video_start, self.controller.shared_data["save_folder_path"])
        except IndexError:
            messagebox.showinfo(message = "Error: Did you choose a folder to save data animation images to?")
        except Exception as e:
            messagebox.showinfo(message = "Error: Did you use proper time stamp format?")
            print(e)
            
class Tab2(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__()
        self.controller = controller

        # --------------- data overlay attributes ------------------------------
        self.video_file_path = ""
        #self.time_stamp = tk.StringVar(value = "%Y-%M-%D %H:%M:%S")
        self.time_stamp = self.controller.shared_data["video_file_start"]
        #self.time_stamp_end = tk.StringVar(value = "%Y-%M-%D %H:%M:%S")
        self.time_stamp_end = self.controller.shared_data["video_file_end"]

        # --------------- data overlay frame -----------------------------------
        self.videofileButton = tk.Button(self, text = "Open Video File", \
                                    command = self.videofileopen)
        self.videofileButton.pack(side = tk.LEFT)
        
        self.trimvideoButton = tk.Button(self, text = "Trim Video", \
                                         command = lambda: \
                                         self.trim_helper(self.time_stamp.get(), \
                                                          self.time_stamp_end.get(), \
                                                          self.video_file_path))
        self.trimvideoButton.pack(side = tk.LEFT)       
        
        self.st_stamp_label = tk.Label(self, text = "Start-Time: ", fg = "blue")
        self.st_stamp_label.pack(side = tk.LEFT)

        #self.time_stamp = tk.StringVar(value = "%Y-%M-%D %H:%M:%S")
        self.stime_stamp_entry = tk.Entry(self, \
                                        textvariable = self.time_stamp)
        self.stime_stamp_entry.pack(side = tk.LEFT)

        self.et_stamp_label = tk.Label(self, text = "End-Time: ", fg = "blue")
        self.et_stamp_label.pack(side = tk.LEFT)

        #self.time_stamp = tk.StringVar(value = "%Y-%M-%D %H:%M:%S")
        self.etime_stamp_entry = tk.Entry(self, \
                                        textvariable = self.time_stamp_end)
        self.etime_stamp_entry.pack(side = tk.LEFT)     

    # tab2 helper -----------------------------------------------------------------------
    def trim_helper(self, start_time, end_time, video_file_path):
        try:
            trim_video(start_time, end_time, video_file_path)
        except ValueError:
            messagebox.showinfo(message = "Error: Did you use proper time stamp format?")
        except CustomError:
            messagebox.showinfo(message = "Error: End Time must be after Start Time.")
        #except Exception as e:
            #print(e)
    
    def videofileopen(self):
        try:
            v = askopenfilename()
            # use videotimestamp method from videotimestamp module
            self.time_stamp.set(str(videotimestamp(v))) #videotimestamp returns datetime.datetime object
            self.time_stamp_end.set(str(videoendtime(v)))
            #self.time_stamp_entry.delete(0, tk.END)
            #self.time_stamp_entry.insert(0, self.time_stamp)
            self.video_file_path = v
        except Exception as e:
            messagebox.showinfo(message = "Error: Did you choose a proper file type?")

class Tab1(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__()
        self.controller = controller
        self.data_file_path = ""
        #self.save_folder_path = ""
        self.df = pandas.DataFrame()

        # --------------- frames --------------------------------------------------------
        self.topframe = tk.Frame(self) #####
        self.topframe.pack(fill = tk.X, side = tk.TOP)
        #topframe.configure(background = "gray")
        self.middleframe = tk.Frame(self) #####
        self.middleframe.pack(fill = tk.X, side = tk.TOP)
        self.middleleftframe = tk.Frame(self.middleframe)
        self.middleleftframe.pack(side = tk.LEFT)
        self.middlemiddleframe = tk.Frame(self.middleframe)
        self.middlemiddleframe.pack(side = tk.LEFT)
        self.middlerightframe = tk.Frame(self.middleframe)
        self.middlerightframe.pack(side = tk.LEFT)
        self.bottomframe = tk.Frame(self) ####
        self.bottomframe.pack(fill = tk.X, side = tk.TOP)
        self.bottomleftframe = tk.Frame(self.bottomframe)
        self.bottomleftframe.pack(side = tk.LEFT)
        self.bottomrightframe = tk.Frame(self.bottomframe)
        self.bottomrightframe.pack(side = tk.LEFT)
        

        # --------------- buttons -------------------------------------------------------
        self.fileButton = tk.Button(self.topframe, text = "Open File", \
                                    command = self.fileopen)
        self.fileButton.pack(side = tk.LEFT)
        self.saveButton = tk.Button(self.topframe, text = "Save to Folder", \
                                    command = self.savefolder)
        self.saveButton.pack(side = tk.LEFT)
        self.createButton = tk.Button(self.topframe, text = "Create Animation", \
                                      command = self.create_animation)
        self.createButton.pack(side = tk.LEFT)
        self.quitButton = tk.Button(self.topframe, text = "Quit", \
                                    command = self.master.destroy) #or self.quit()
        self.quitButton.pack(side = tk.LEFT)

        # ---------------- labels -------------------------------------------------------
        self.x_axis_label = tk.Label(self.middleleftframe, text = "X-Axis: ", fg = "blue")
        self.x_axis_label.pack(side = tk.LEFT)
        self.y_axis_label = tk.Label(self.middlemiddleframe, text = "Y-Axis: ", fg = "blue")
        self.y_axis_label.pack(side = tk.LEFT)
        self.t_axis_label = tk.Label(self.middlerightframe, text = "Time-Axis: ", fg = "blue")
        self.t_axis_label.pack(side = tk.LEFT)       

        self.x_axis_title_label = tk.Label(self.bottomleftframe, \
                                           text = "X-Axis Title: ", fg = "blue")
        self.x_axis_title_label.pack(side = tk.LEFT)
        self.y_axis_title_label = tk.Label(self.bottomrightframe, \
                                           text = "Y-Axis Title: ", fg = "blue")
        self.y_axis_title_label.pack(side = tk.LEFT)

        # ---------------- entry -------------------------------------------------------
        self.x_axis_title = tk.StringVar()
        self.x_axis_title_entry = tk.Entry(self.bottomleftframe, \
                                        textvariable = self.x_axis_title)
        self.x_axis_title_entry.pack(side = tk.LEFT)

        self.y_axis_title = tk.StringVar()
        self.y_axis_title_entry = tk.Entry(self.bottomrightframe, \
                                        textvariable = self.y_axis_title)
        self.y_axis_title_entry.pack(side = tk.LEFT)       
        
        # ---------------- drop down menus ----------------------------------------------
        # X-Axis:
        self.selected_x_axis = tk.StringVar(self.middleleftframe) #track what x_axis_menu is set to
        self.x_axis_options = [None]
        self.selected_x_axis.set(self.x_axis_options[0])
        self.x_axis_menu = tk.OptionMenu(self.middleleftframe, self.selected_x_axis, \
                                         *self.x_axis_options)
        self.x_axis_menu.pack(side = tk.LEFT)

        # Y-Axis
        self.selected_y_axis = tk.StringVar(self.middlemiddleframe) #track what y_axis_menu is set to
        self.y_axis_options = [None]
        self.selected_y_axis.set(self.y_axis_options[0])
        self.y_axis_menu = tk.OptionMenu(self.middlemiddleframe, self.selected_y_axis, \
                                         *self.y_axis_options)
        self.y_axis_menu.pack(side = tk.LEFT)

        # Time-Axis
        self.selected_t_axis = tk.StringVar(self.middlerightframe) #track what t_axis_menu is set to
        self.t_axis_options = [None]
        self.selected_t_axis.set(self.t_axis_options[0])
        self.t_axis_menu = tk.OptionMenu(self.middlerightframe, self.selected_t_axis, \
                                         *self.t_axis_options)
        self.t_axis_menu.pack(side = tk.LEFT)
    
    # helpers ---------------------------------------------------------------------------
    def fileopen(self):
        "open file and update df and menu options"
        try:
            self.data_file_path = tk.filedialog.askopenfile()
            try:
                self.df = pandas.read_csv(self.data_file_path)
            except:
                try:
                    self.df = pandas.read_excel(self.data_file_path.name)
                    try:
                        x = creationdate(self.data_file_path.name)
                        self.controller.shared_data["data_file_creation"].set(x)
                    except Exception as e:
                        print(e)
                except:
                    raise
        except Exception as e:
            messagebox.showinfo(message = "Error: Did you choose proper " + \
                                "file type (Excel or csv)?")
        self.update_dropdown_menus()
            
    def update_dropdown_menus(self):
        try:
            self.set_x_axis_options(list(self.df.columns.values))
            self.set_x_axis_menu()
            self.set_y_axis_options(list(self.df.columns.values))
            self.set_y_axis_menu()
            self.set_t_axis_options(list(self.df.columns.values))
            self.set_t_axis_menu()           
        except:
            pass

    def savefolder(self):
        "choose folder to save images too"
        self.controller.shared_data["save_folder_path"] = tk.filedialog.askdirectory()

    def create_animation(self):
        try:
            # start of gui access ----------------------------------------------------------
            TABLE = self.get_df() # dataframe from file chosen in gui
            usr_x_axis = self.selected_x_axis.get() # x_axis chosen in gui
            usr_y_axis = self.selected_y_axis.get() # y_axis chosen in gui
            usr_t_axis = self.selected_t_axis.get() # t_axis chosen in gui
            usr_x_axis_title = self.x_axis_title.get() # x_axis title from gui
            usr_y_axis_title = self.y_axis_title.get() # y_axis title from gui
            # end of gui access ------------------------------------------------------------

            # clean relevant series of data that can't be converted to numeric -------------
            TABLE.loc[:, usr_t_axis] = pandas.to_numeric(TABLE[usr_t_axis], errors = 'coerce')
            try: # user is not required to choose both x-axis and y-axis
                TABLE.loc[:, usr_x_axis] = pandas.to_numeric(TABLE[usr_x_axis], errors = 'coerce')
            except:
                pass
            try:
                TABLE.loc[:, usr_y_axis] = pandas.to_numeric(TABLE[usr_y_axis], errors = 'coerce')
            except:
                pass
            try:
                TABLE.dropna(subset = [usr_t_axis, usr_x_axis, usr_y_axis], \
                             inplace = True) # dropna values without create df copy
            except:
                try:
                    TABLE.dropna(subset = [usr_t_axis, usr_x_axis], \
                             inplace = True) # dropna values without create df copy
                except:
                    TABLE.dropna(subset = [usr_t_axis, usr_y_axis], \
                             inplace = True) # dropna values without create df copy
            # end of cleaning series --------------------------------------------------------
                    
            # convert time series to int for handling purposes. 
            TABLE[usr_t_axis] = TABLE[usr_t_axis].astype(int)
            # Set up the empty figure and subplot we want to animate on
            fig = plt.figure()
            ax1 = fig.add_subplot(1,1,1)

            
            #Pass number of frames to 'animate' that is equivalent to max number of seconds
            #from Data.csv
            #for some reason 0 is called twice so we need to add an extra frame in order
            #to get last data point
            FRAMES = TABLE[usr_t_axis].astype(int).max() + 1
            self.controller.shared_data["data_file_end"].set(str(FRAMES)) # update shared IntVar()

            #FuncAnimation will animate to 'fig' based on function passed to it
            #called 'animate'. Every 'interval' (1000 ms) 'animate' will be called.
            #'interval' is also the delay between 'frames'.
            #'repeat' = False because we don't want animation to repeat when the sequence of
            #'frames' is completed.
            xs = [] # initialized lists to pass to animate()
            ys = []
            ani = animation.FuncAnimation(fig, animate, interval = 1000, frames = FRAMES, \
                                          fargs = (xs, ys, usr_x_axis, usr_x_axis_title,
                                                   usr_y_axis, usr_y_axis_title, usr_t_axis, \
                                                   fig, ax1, TABLE, \
                                                   self.controller.shared_data["save_folder_path"]), \
                                                   repeat = False)

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
            messagebox.showinfo(message = "Error: Must choose Time-axis" + \
                                " and either X-axis or Y-axis from dropdown menus.")

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
        
class DataAnimationGui:
    def __init__(self, master):
        self.shared_data = {"data_file_creation": tk.StringVar(), "data_file_end": tk.StringVar(), \
                            "video_file_start": tk.StringVar(), "video_file_end": tk.StringVar(), \
                            "save_folder_path": ""}
        self.shared_data["data_file_creation"].set("%Y-%M-%D %H:%M:%S")
        self.shared_data["data_file_end"].set("N/A")
        self.shared_data["video_file_start"].set("%Y-%M-%D %H:%M:%S")
        self.shared_data["video_file_end"].set("%Y-%M-%D %H:%M:%S")
        master.wm_title("DataAnimationGui")

        # --------------- tabs -------------------------------------------------
        tabControl = ttk.Notebook(master)
        tab1 = Tab1(tabControl, self)
        tabControl.add(tab1, text = "Easy Data Animation")
        tab2 = Tab2(tabControl, self)
        tabControl.add(tab2, text = "Video Upload/Trim")
        tab3 = Tab3(tabControl, self)
        tabControl.add(tab3, text = "Data Animation and Video Sync")
        tabControl.pack(expand = 1, fill = "both")
        

def data_for_animate(time, x_axis, y_axis, t_axis, df):
    "returns xs and ys from df as of 'time' to be plotted in 'animate'"
    try: # if x-axis wasn't chosen by user, then use index
        X_series = df[df[t_axis] == time][x_axis] # linked to gui
    except:
        X_series = df[df[t_axis] == time].index
    X_list = X_series.tolist()

    try: # if y-axis wasn't chosen by user, then use index
        Y_series = df[df[t_axis] == time][y_axis] # linked to gui
    except:
        Y_series = df[df[t_axis] == time].index
    Y_list = Y_series.tolist()
    
    return X_list, Y_list

def animate(interval, xs, ys, x_axis, x_axis_title, y_axis, y_axis_title, t_axis, \
            figure, subplot, data_frame, folder_path):
    """plot data from data_frame on subplot as of time = 'interval'
       xs = []
       ys = []
       x_axis, y_axis are column headers of data_frame that animate
                      will plot against each other 
    """

    time = interval #interval is number of times 'animate' has been called
                    #by FuncAnimation

    if time in data_frame[t_axis].unique(): # if 'time' is a datapoint in df then plot data
        X, Y = data_for_animate(time, x_axis, y_axis, t_axis, data_frame)
        xs.extend(X) #extend list X to end of list xs
        ys.extend(Y)
        subplot.clear() # clear the subplot
        subplot.scatter(xs, ys)
        subplot.set_xlabel(x_axis_title, fontweight = 'bold')
        subplot.set_ylabel(y_axis_title, fontweight = 'bold')
        # DataFrame.items() returns zip object. Convert to list, access [0][1],
        # then convert to string
        subplot.set_title(str(list(data_frame[data_frame[t_axis] == time][t_axis].items())[0][1]) \
                          + 's', fontweight = 'bold')
    # save figure EVERY time animate() is called
    try:
        figure.savefig(str(folder_path) + '/' + str(time) + '.png')
    except:
        figure.savefig(str(time) + '.png')
    return

if __name__ == "__main__":
    main()
