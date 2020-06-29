import csv

class leapMotionSensor:
    def __init__(self):
        print("leapMotionSenson object init")
        self.prev_received_Data_from_leap = -1
        self.thresholdIgnoreError = 1
        self.isError = 0
        self.blockTheSignal = 0
        self.blockNumber = 10000

    def receiveData(self):
        lst = [0, 0, 0, 0]
        with open('test.csv', 'r') as file:
            reader = csv.reader(file)
            for row, x in enumerate(reader):
                if row > 3 or row < 0:
                    row = 3
                lst[row] = int(float(x[0]))
        result = -1
        if (lst[0] == 0 and lst[1] == 0 and lst[2] == 0):
            result = -1
        elif (lst[0] < -40 and (-40 < lst[1] < 40) and (-40 < lst[2] < 40)):
            result = 1
        elif (lst[1] < -40 and (-40 < lst[0] < 40) and (-40 < lst[2] < 40)):
            result = 2
        elif (lst[2] < -40 and (-40 < lst[1] < 40) and (-40 < lst[0] < 40)):
            result = 3

        resultInt = int(result)

        print("the leap motion value is", resultInt)

        if self.blockTheSignal > 0:
            self.blockTheSignal -= 1
            return -1
        else:
            if resultInt != -1:
                self.blockTheSignal = self.blockNumber

        return resultInt