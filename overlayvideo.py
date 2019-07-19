import moviepy.editor as mpe
from PIL import Image
import numpy as np

import os
import glob
from datetime import datetime

#https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
def combine_images(a, b):
    """"combines two Pillow Images and returns one.
    'a' on left - original size is preserved
    'b' on right - original size is preserved """
    
    images = [a, b]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    return new_im

def overlay_video(figure, video_clip):
    """places figure on left hand side of video_clip"""

    new_frames = []

    for frame in video_clip.iter_frames():
        # convert frame to PIL image
        a = Image.fromarray(frame)
        # combine PIL images into one
        # this seems to be the root cause of error with .mov 
        b = combine_images(figure, a)
        # convert from PIL image to frame
        c = np.array(b)
        new_frames.append(c)

    new_clip = mpe.ImageSequenceClip(new_frames, fps = video_clip.fps)
    #put audio back into new_clip
    new_clip = new_clip.set_audio(video_clip.audio)
    # quicktime does not support moviepy default codec
    # therefore, sound is only heard if checked with VLC Media Player
    return new_clip

#alternative method to overlay_video that I could not get to work but
#may be more efficient
"""
def overlay_video_b(figure, video_clip):
    modified_clip = video_clip.fl_image(lambda image: combine_images(image, figure))
"""
"""
figure = Image.open("0.png")
clip = mpe.VideoFileClip("trim_test.mp4")
# prevent moviepy from automatically converting portrait to landscape
if clip.rotation == 90:
    clip = clip.resize(clip.size[::-1])
    clip.rotation = 0
new_clip = overlay_video(figure, clip)
new_clip.write_videofile("new_file.mp4")
"""

def video_array(clip1, clip2, audio):
    """generates new video clip which is an clips.array of the two video clips
    passed to the function. accepts audio parameter as well"""

    clip = mpe.clips_array([[clip1, clip2]])
    clip = clip.set_audio(audio)

    return clip

def sync_videos(data_start, video_start):

    print(data_start)
    print(video_start)

    data_start_datetime = datetime.strptime(data_start, '%Y-%m-%d %H:%M:%S')
    video_start_datetime = datetime.strptime(video_start, '%Y-%m-%d %H:%M:%S')

    delta = (data_start_datetime - video_start_datetime).total_seconds()
    print(delta)
    
    
    image_list = []
    #append file names from Output_Images as strings to image_list
    for root, dirs, files in os.walk('Output_Images'):
        image_list += glob.glob(os.path.join(root, '*png'))

    image_list.sort() #sort list by file name


    data_clip = mpe.ImageSequenceClip(image_list, fps = 1)
    video_clip = mpe.VideoFileClip("trim_test.mp4")
    # prevent moviepy from automatically converting portrait to landscape
    if video_clip.rotation == 90:
        video_clip = video_clip.resize(video_clip.size[::-1])
        video_clip.rotation = 0

    # relevant attributes for composition
    test = data_clip.set_start(delta, change_end = True)
    test.end += delta # this didn't seem to work
    test.duration += delta # this worked!
    
    final_clip = video_array(test, \
                             video_clip, video_clip.audio)
    final_clip.write_videofile("sync_test.mp4")
    
