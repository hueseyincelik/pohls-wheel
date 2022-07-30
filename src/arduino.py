import serial


class Arduino:
    def __init__(self, port, rate):
        self.port = port
        self.rate = rate
        self.arduino = serial.Serial(port=self.port, baudrate=self.rate)

    def reconnect(self):
        self.arduino = serial.Serial(port=self.port, baudrate=self.rate)

    def read(self):
        return self.arduino.readline()

    def write(self, value, encoding="UTF-8"):
        self.arduino.write(bytes(value, encoding))
