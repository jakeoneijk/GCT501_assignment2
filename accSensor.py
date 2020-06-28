#ssh pi@192.168.1.248
from socket import *
class accSensor:
    def __init__(self):
        self.ip = '192.168.1.248'
        self.port = 8080
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        self.clientSock.connect((self.ip, self.port))
        print('연결 확인 됐습니다.')
        self.clientSock.send('I am a client'.encode('utf-8'))
        print('메시지를 전송했습니다.')
        data = self.clientSock.recv(1024)
        print('받은 데이터 : ', data.decode('utf-8'))

        self.blockTheSignal = 0
        self.blockNumber = 5

    def receiveData(self):  # return -1: no acc motion , 0 : verticalMotion , 1: horizontalMotion , 2: circleMotion
        # 1 stop - 1, 0 motion 0 , 3 motion 1 , 2 motion 2
        receive = self.clientSock.recv(1024)[0]
        print("receiveAccSensor : ", receive)
        if (receive % 2) == 1:
            receive = receive - 2
        if receive == 2:
            receive = 0

        if self.blockTheSignal > 0:
            self.blockTheSignal -= 1
            return -1
        else:
            if receive != -1:
                self.blockTheSignal = 5

        return receive
