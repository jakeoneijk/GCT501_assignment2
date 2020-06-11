import pygame as pg
import time

soundType = {'ORIGINAL':0 , 'REVERB':1 , 'DISTORTED':2}
motionType = {'verticalMotion':0 , 'horizontalMotion':1,'circleMotion':2}

soundDir = []
soundDir.append(["flute-A4.wav","cello-double.wav"])    #original sound dir
soundDir.append([])                                     #reverb sound dir
soundDir.append([])                                     #distorted sound dir

sound = []

def initiate(): #store the sound
    pg.mixer.init()
    pg.init()
    for i in range(0,len(soundDir)):
        sound.append([])
        for j in range(0,len(soundDir[i])):
            sound[i].append(pg.mixer.Sound(soundDir[i][j]))
    pg.mixer.set_num_channels(50)

def playTheSound(type , index):
    sound[type][index].play()
    time.sleep(0.3)

initiate()

playTheSound(soundType['ORIGINAL'],0)
playTheSound(soundType['ORIGINAL'],1)


time.sleep(5)
