import time
import serial

class SerialConnection:
    def __init__(self, port, speed):
        self.port = port
        self.speed = speed
        self.timeout = 0.5
        self.obj = None

    def open(self):
        self.obj = serial.Serial(self.port, self.speed)

        if self.obj.is_open:
            print("Device connected")
            self.readOutput()

    def close(self):
        self.obj.close()

    def run(self, command):
        if self.obj is not None:
            if self.obj.is_open:
                self.obj.write((command + "\r\n").encode())
                time.sleep(self.timeout)
                self.readOutput()
            else:
                print("ERROR: connection is not opened")
        else:
            print("ERROR: communication object does not exist")

    def readOutput(self):
        output = str()

        while self.obj.inWaiting() > 0:
            output += self.obj.read(1).decode()

        if len(output):
            print(output)

def main():
    x = SerialConnection("COM4", "115200")
    x.open()
    x.run("root")
    x.run("root")
    x.run("ls -a")
    x.run("ls -a")
    x.run("ls -a")
    x.close()

if __name__ == '__main__':
    main()
