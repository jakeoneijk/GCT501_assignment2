import csv

class leapMotionSensor:
    def __init__(self):
        print("leapMotionSenson object init")
        self.prev_received_Data_from_leap = -1

    def receiveData(self):
        lst = [0, 0, 0, 0]
        with open('test.csv', 'r') as file:
            reader = csv.reader(file)
            for row, x in enumerate(reader):
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

        if resultInt != self.prev_received_Data_from_leap:
            self.prev_received_Data_from_leap = resultInt
            return resultInt
        else:
            return -1