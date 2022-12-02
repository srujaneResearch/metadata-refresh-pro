from moviepy.editor import *


clip = VideoFileClip("test.avi", audio=False)


l = clip.on_color()