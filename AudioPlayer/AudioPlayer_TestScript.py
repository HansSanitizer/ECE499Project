""" This Script Tests the functionality of the AudioPlayer module.

    Warning: there is a very real danger of screaming feedback, so
             lower speaker volume before using!
"""
from AudioPlayer import AudioPlayer

player = AudioPlayer.AudioPlayer()

player.load("/Users/nolanmeske/Documents/Music Projects/4280/Orbital/renders/Orbital.wav")
player.play()
del player
