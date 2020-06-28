import pygame as pg
import time

#ssh pi@192.168.1.248

from socket import *
clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.1.248', 8080))
print('연결 확인 됐습니다.')
clientSock.send('I am a client'.encode('utf-8'))
print('메시지를 전송했습니다.')
data = clientSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

soundType = {'ORIGINAL':0 , 'REVERB':1 , 'DISTORTED':2 , 'REVERBandDISTORTED':3}
motionType = {'verticalMotion':0 , 'horizontalMotion':1,'circleMotion':2}

#accSensorCount = [0,0,0]
blockTheSignal = 0

distortedActivated = 0
reverbActivated = 0

soundDir = []
soundDir.append(["./sound/normal_kick.wav","./sound/normal_snare.wav","./sound/normal_purcu.wav","./sound/normal_synth.wav"])    #original sound dir
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
    time.sleep(0.01)

def receiveLeap(): # return -1: no leapmotion , 1: leapmotion activated
    print("receiveLeapMotion")
    return -1

#def initAccSensorCount():
#    accSensorCount[0] = 0
#    accSensorCount[1] = 0
#    accSensorCount[2] = 0

def receiveAccSensor(): # return -1: no acc motion , 0 : verticalMotion , 1: horizontalMotion , 2: circleMotion
    # 1 stop - 1, 0 motion 0 , 3 motion 1 , 2 motion 2
    global blockTheSignal
    receive = clientSock.recv(1024)[0]
    print("receiveAccSensor : ",receive)
    if (receive  % 2) == 1:
        receive = receive -2
    if receive == 2:
        receive = 0

    if blockTheSignal > 0:
        blockTheSignal = blockTheSignal - 1
        return  -1
    else:
        if receive != -1:
            blockTheSignal = 5

    return receive

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
