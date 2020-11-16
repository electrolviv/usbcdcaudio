import platform

import serial
from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLineEdit, QPushButton


class WidgetSelectSerialPort(QWidget):

    def __init__(self):
        super(WidgetSelectSerialPort, self).__init__()

        self.serial = serial.Serial()

        self.gbox = QGroupBox("Serial Port")

        self.lineEditComport = QLineEdit()
        port = "COM4" if platform.system() == "Windows" else "/dev/ttyACM0"
        self.lineEditComport.setText(port)

        self.pushButtonReconnect  = QPushButton("Connect")

        self.setLayout(self.genlayout())


    def genlayout(self):
        self.gbox.setLayout(self.genlayout_gbox())
        lay = QHBoxLayout()
        lay.addWidget(self.gbox)
        return lay

    def genlayout_gbox(self):
        lay = QHBoxLayout()
        lay.addWidget(self.lineEditComport)
        lay.addWidget(self.pushButtonReconnect)
        return lay

    def isSerialPortOpen(self) -> bool:
        return self.serial.isOpen()

    def ReopenPort(self):

        try:
            baudrate = 1000000
            self.serial = serial.Serial(self.lineEditComport.text(), baudrate)
            print("Opened")

        except serial.serialutil.SerialException:
            pass
