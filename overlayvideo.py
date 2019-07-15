import moviepy.editor as mpe
from PIL import Image
import numpy as np

#https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
def combine_images(a, b):
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


figure = Image.open("0.png")
square_figure = figure.resize((100, 100))

clip = mpe.VideoFileClip("Sample9.mp4")



#print([frame[0, :, 0].max() for frame in clip.iter_frames()])

#print(type(clip.get_frame(1)))

#print(clip.get_frame(1).shape)

new_frames = []

for frame in clip.iter_frames():
    # convert frame to PIL image
    a = Image.fromarray(frame)
    #a.paste(square_figure, (0, 0, 100, 100))
    #a.show()
    # convert from PIL image to frame
    a = combine_images(figure, a)
    a = np.array(a)
    new_frames.append(a)

new_clip = mpe.ImageSequenceClip(new_frames, fps = clip.fps)
#put audio back into new_clip
new_clip = new_clip.set_audio(clip.audio)
# quicktime does not support moviepy default codec
# therefore, sound is only heard if checked with VLC Media Player
new_clip.write_videofile("new_file.mp4")
    

