import moviepy.editor as mpe
from PIL import Image
import numpy as np

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

    for frame in clip.iter_frames():
        # convert frame to PIL image
        a = Image.fromarray(frame)
        # combine PIL images into one
        a = combine_images(figure, a)
        # convert from PIL image to frame
        a = np.array(a)
        new_frames.append(a)

    new_clip = mpe.ImageSequenceClip(new_frames, fps = video_clip.fps)
    #put audio back into new_clip
    new_clip = new_clip.set_audio(video_clip.audio)
    # quicktime does not support moviepy default codec
    # therefore, sound is only heard if checked with VLC Media Player
    return new_clip

figure = Image.open("0.png")
clip = mpe.VideoFileClip("IMG_3816.MOV")
new_clip = overlay_video(figure, clip)
new_clip.write_videofile("new_file.mp4")
    

