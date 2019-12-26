# dataanimation
auto-generates plot animation of data (one graph plot per second) and can synchronize plot animation with video footage based off of video metadata timestamp and timestamps of data. It can be useful to visualize any data that was generated alongside the filming of the desired event (for example, visualizing sensor data that was collected during the filming of an experiment). 

**Once you have cloned the directory to your local machine, follow the directions below:**
1. cd into dataanimation directory
2. $pipenv install
3. $pipenv run python dataanimation.py

**Data Animation**
![Alt text](https://github.com/thomasmatt88/dataanimation/blob/master/images/Screen%20Shot%202019-12-26%20at%202.02.13%20PM.png)
<br>
Open File: Upload csv or excel file. 
<br>
Save to Folder: Choose folder to save images to (data animation output is a collection of matplotlib images). 
<br>
X-Axis: Choose X-axis column of data
<br>
Y-Axis: Choose Y-axis column of data
<br>
Time-Axis: Choose Time-axis column of data
<br>
X-Axis Title: Type in desired X-axis header
<br>
Y-Axis Title: Type in desired Y-axis header
<br>
Create Animation: Create plot animation after all parameters have been set
<br>
Quit: Close GUI and quit program

![Alt text](https://github.com/thomasmatt88/dataanimation/blob/master/images/Screen%20Shot%202019-12-26%20at%202.04.11%20PM.png)
**Video Upload/Trim**
<br>
Open Video File: Upload video to be synced with data animation
<br>
Start-Time: timestamp for start of video
<br>
End-Time: timestamp for end of video
<br>
Trim Video: Trim video within the desired 'Start-Time' and 'End-Time'

![Alt text](https://github.com/thomasmatt88/dataanimation/blob/master/images/Screen%20Shot%202019-12-26%20at%202.11.09%20PM.png)
**Data Animation and Video Sync**
<br>
Data animation is the collection of plot images that are created and saved to desired folder using 'Easy Data Animation' tab
<br>
Data Start-Time: timestamp for start of data animation
<br>
Sync Video: Sync data animation with trimmed video created using 'Video Upload/Trim' tab
