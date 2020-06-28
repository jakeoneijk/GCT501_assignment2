import leapMotionSensor
import playSound
import accSensor

class controller:
    def __init__(self):
        self.leapmotion = leapMotionSensor.leapMotionSensor()
        self.play_sound = playSound.playSound()
        self.acc = accSensor.accSensor()
        self.prev_received_Data_from_leap = -1

    def processLeapMotinoData(self, received_data):
        if received_data != self.prev_received_Data_from_leap:
            if received_data == 3:
                self.play_sound.playTheSynthSound()
        self.prev_received_Data_from_leap = received_data

    def processAccData(self,received_data):
        if received_data != -1:
            self.play_sound.playTheSound(received_data)

    def mainProcess(self):
        while True:
            receive_from_leap = self.leapmotion.receiveData()
            receive_from_acc = self.acc.receiveData()
            self.processLeapMotinoData(receive_from_leap)
            self.processAccData(receive_from_acc)