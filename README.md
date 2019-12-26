# dataanimation
auto-generates plot animation of data (one graph image per second) and can synchronize plot animation with video footage based off of video metadata timestamp

**Once you have cloned the directory to your local machine, follow the directions below:**
1. cd into dataanimation directory
2. $pipenv install
3. $pipenv run python dataanimation.py

**Data Animation**
Open File: Upload csv or excel file. 
Save to Folder: Choose folder to save images to (data animation output is a collection of matplotlib images). 
X-Axis: Choose X-axis column of data
Y-Axis: Choose Y-axis column of data
Time-Axis: Choose Time-axis column of data
X-Axis Title: Type in desired X-axis header
Y-Axis Title: Type in desired Y-axis header
Create Animation: Create plot animation after all parameters have been set
Quit: Close GUI and quit program

**Video Upload/Trim**
Open Video File: Upload video to be synced with data animation
Start-Time: timestamp for start of video
End-Time: timestamp for end of video
Trim Video: Trim video within the desired 'Start-Time' and 'End-Time'

**Data Animation and Video Sync**
Data animation is the collection of plot images that are created and saved to desired folder using 'Easy Data Animation' tab
Data Start-Time: timestamp for start of data animation
Sync Video: Sync data animation with trimmed video created using 'Video Upload/Trim' tab
