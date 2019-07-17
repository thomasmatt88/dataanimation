from hachoir.metadata import extractMetadata
from datetime import datetime
import moviepy.editor as mpe

# custom modules
from videotimestamp import videotimestamp

def trim_start(new_start_time, video_file_path):

    #convert new_start_time to datetime object
    new_start_time = datetime.strptime(new_start_time, '%Y-%m-%d %H:%M:%S')

    #returns datetime object
    video_creation_datetime = videotimestamp(video_file_path)
    
    #subtract video creation date from data start date and end date in order to get elapsed times
    #convert elapsed timedelta objects into floats
    start_time_seconds = (new_start_time - video_creation_datetime).total_seconds()
    

    #trim video based off of start time and end time
    clip = mpe.VideoFileClip(video_file_path)
    #prevent moviepy from automatically converting portrait to landscape
    if clip.rotation == 90:
        clip = clip.resize(clip.size[::-1])
        clip.rotation = 0
    clip.ffmpeg_params = ['-noautorotate'] #doesn't seem to do anything
    # trim clip
    final_clip = clip.subclip(t_start = int(start_time_seconds))
    return final_clip, start_time_seconds

def trim_end(new_end_time, video_file_path, video_clip, start):

    new_end_time = datetime.strptime(new_end_time, '%Y-%m-%d %H:%M:%S')
    video_creation_datetime = videotimestamp(video_file_path)
    end_time_seconds = (new_end_time - video_creation_datetime).total_seconds() \
                       - start
    clip = video_clip
    if clip.rotation == 90:
        clip = clip.resize(clip.size[::-1])
        clip.rotation = 0
    clip.ffmpeg_params = ['-noautorotate'] #doesn't seem to do anything
    # trim clip
    final_clip = clip.subclip(t_start = 0, t_end = int(end_time_seconds))
    return final_clip

def trim_video(new_start_time, new_end_time, video_file_path):
    clip, start = trim_start(new_start_time, video_file_path)
    clip = trim_end(new_end_time, video_file_path, clip, start)
    save_video_clip(clip, "trim_test.mp4")
    

def save_video_clip(video_clip, file_name):
    """saves videoclip into file with optimal settings for youtube"""
    
    video_clip.ffmpeg_params = ['-noautorotate'] #doesn't seem to do anything
    # recommended settings for youtube
    video_clip.write_videofile(filename = file_name, \
                                      codec = "libx264", audio_codec = "aac")
                                    #bitrate = 10 Mbps for 30 FPS and 15 Mbps for 60 fps
   
