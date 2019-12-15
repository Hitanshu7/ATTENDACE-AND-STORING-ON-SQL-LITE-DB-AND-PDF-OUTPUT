"""
utility file to create sound
just pass the text you want to convert to sound to the generate_sound_file function.
"""
from gtts import gTTS
import os


def generate_sound_file(text):
    filename = "_".join(text.strip().split(" "))
    myObj = gTTS(text=text, lang="en", slow=False)
    myObj.save("media/{}.mp3".format(filename))

if not os.path.exists("media"):
    os.mkdir("media") 
generate_sound_file("Try again")