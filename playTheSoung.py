import pygame as pg
import time

#ssh pi@192.168.1.248

soundType = {'ORIGINAL':0 , 'REVERB':1 , 'DISTORTED':2 , 'REVERBandDISTORTED':3}
motionType = {'verticalMotion':0 , 'horizontalMotion':1,'circleMotion':2}

distortedActivated = 0
reverbActivated = 0

soundDir = []
soundDir.append(["./sound/dis_kic.wav"])    #original sound dir
soundDir.append([])                                     #reverb sound dir
soundDir.append([])                                     #distorted sound dir
soundDir.append([])                                     #distorted reverb sound dir
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

def receiveLeap(): # return -1: no leapmotion , 1: leapmotion activated
    print("receiveLeapMotion")
    return -1

def receiveAccSensor(): # return -1: no acc motion , 0 : verticalMotion , 1: horizontalMotion , 2: circleMotion
    print("receiveAccSensor")
    return 0

def receiveLightSensor(): # return -1: no lightmotion , 1: lightmotion activated
    print("receiveLightSensorSensor")
    return -1

initiate()

while True:
    if receiveLeap() == 1:
        distortedActivated = (distortedActivated+1)%2
    if receiveLightSensor() == 1:
        reverbActivated = (reverbActivated+1)%2
    accSensorOutput = receiveAccSensor()
    if accSensorOutput != -1:
        if (reverbActivated == 1) and (distortedActivated == 1):
            playTheSound(soundType['REVERBandDISTORTED'], accSensorOutput)
        elif (reverbActivated == 1):
            playTheSound(soundType['REVERB'], accSensorOutput)
        elif distortedActivated == 1:
            playTheSound(soundType['DISTORTED'], accSensorOutput)
        else :
            playTheSound(soundType['ORIGINAL'], accSensorOutput)


#playTheSound(soundType['ORIGINAL'],0)
#playTheSound(soundType['ORIGINAL'],1)
#time.sleep(5)
