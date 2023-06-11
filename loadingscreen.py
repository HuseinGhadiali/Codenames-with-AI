import vlc
import time
from tkinter import *

def play_video():
    # Create a tkinter window
    root = Tk()
    root.geometry("800x600")

    # Create a VLC instance
    instance = vlc.Instance()

    # Create a VLC media player
    player = instance.media_player_new()

    # Load the video file
    media = instance.media_new("Codenames/Codenamesloading.mp4")

    # Set the media for the player
    player.set_media(media)

    # Play the video
    player.play()

    # Wait for the video to finish playing
    while player.get_state() != vlc.State.Ended:
        time.sleep(1)

    # Close the tkinter window
    root.destroy()

    root.mainloop()
