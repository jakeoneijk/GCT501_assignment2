import pygame as pg
import time

class playSound:
    def __init__(self):
        self.distortedActivated = 0
        self.reverbActivated = 0
        self.synthOrder = 0
        self.type = 0

        self.soundType = {'ORIGINAL': 0, 'REVERB': 1, 'DISTORTED': 2, 'REVERBandDISTORTED': 3}
        self.motionType = {'verticalMotion': 0, 'horizontalMotion': 1, 'circleMotion': 2}
        self.soundDir = []
        self.soundDir.append(["./sound/normal_kick.wav", "./sound/normal_snare.wav", "./sound/normal_purcu.wav","./sound/synth1.wav","./sound/synth2.wav"])  # original sound dir
        self.soundDir.append(["./sound/r_kick.wav","./sound/r_snare.wav","./sound/r_p.wav","./sound/R_synth1.wav","./sound/R_synth2.wav"])  # reverb sound dir
        self.soundDir.append(["./sound/dis_kic.wav","./sound/dis_snare.wav","./sound/dis_pur.wav","./sound/D_synth1.wav","./sound/D_synth2.wav"])  # distorted sound dir
        self.soundDir.append(["./sound/rd_kick.wav","./sound/rd_snare.wav","./sound/rd_purcussion.wav","./sound/RD_synth1.wav","./sound/RD_synth2.wav"])  # distorted reverb sound dir
        self.sound = []

        pg.mixer.init()
        pg.init()
        for i in range(0, len(self.soundDir)):
            self.sound.append([])
            for j in range(0, len(self.soundDir[i])):
                self.sound[i].append(pg.mixer.Sound(self.soundDir[i][j]))
        pg.mixer.set_num_channels(50)

    def playTheSound(self, index):
        self.sound[self.type][index].play()
        time.sleep(0.01)

    def playTheSynthSound(self):
        self.sound[self.type][3+self.synthOrder].play()
        time.sleep(0.01)
        self.synthOrder += 1