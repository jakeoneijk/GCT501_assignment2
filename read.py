import csv

lst = [0,0,0,0]
a = 0

while True: 
    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        for row,x in enumerate(reader):
            lst[row] = int(float(x[0]))
    
    if(lst[0]==0 and lst[1] == 0 and lst[2] == 0):
        a = -1
    elif(lst[0]<-40 and (-40<lst[1]<40) and (-40<lst[2]<40)):
        a = 1
    elif(lst[1]<-40 and (-40<lst[0]<40) and (-40<lst[2]<40)):
        a = 2
    elif(lst[2]<-40 and (-40<lst[1]<40) and (-40<lst[0]<40)):
        a = 3

    print("the value is", a)
    

