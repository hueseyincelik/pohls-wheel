from serial import Serial


class Arduino:
    def __init__(self, port, rate=115200):
        self.port, self.rate = port, rate
        self.arduino = Serial(port=self.port, baudrate=self.rate)

    def reconnect(self):
        self.arduino = Serial(port=self.port, baudrate=self.rate)

    def read(self):
        return self.arduino.readline()

    def write(self, value, encoding="UTF-8"):
        self.arduino.write(bytes(value, encoding))
