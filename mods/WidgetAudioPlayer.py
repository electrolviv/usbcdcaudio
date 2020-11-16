import os
import platform
from typing import Dict

import serial

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QFrame, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from WidgetAudioStat import WidgetAudioStat
from WidgetBuffer import WidgetBuffer
from WidgetMP3Frames import WidgetMP3Frames
from WidgetPosition import WidgetPosition
from WidgetSelectFile import WidgetSelectFile
from WidgetSerialPort import WidgetSelectSerialPort
from WidgetStereoOsc import WidgetStereoOsc
from mods.audiofile import AudioFile


class WidgetAudioPlayer(QWidget):

    class Runtimestat:
        updateuicnt = 0
        sentbytes   = 0



    def __init__(self):

        super(WidgetAudioPlayer, self).__init__()

        # Global Objects
        self.afile = AudioFile()

        # setup
        self.timerrate = 10  # ms
        self.guirate   = 3   # xtimerrate


        self.setWindowTitle("MP3-USB Audio Player")

        self.label_title = QLabel("USB CDC MP3 Audio Player")
        self.label_title.setAlignment( Qt.AlignTop | Qt.AlignCenter )
        self.label_title.setFixedHeight(42)
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setFont(QFont('Arial', 14, 200, True))

        self.wdgAudioStat = WidgetAudioStat()
        self.wdgSelectFile = WidgetSelectFile(self.on_file_selected)
        self.wdgPosition = WidgetPosition()
        self.wdgSerialPort = WidgetSelectSerialPort()
        self.wdgBuffer = WidgetBuffer()
        self.wdgOscLR = WidgetStereoOsc()

        self.wdgChunks = WidgetMP3Frames()

        self.setLayout(self.genlayout())

        self.timer10ms = QtCore.QTimer(self)
        self.timer10ms.timeout.connect(self.timerevent)
        self.timer10ms.setSingleShot(False)
        self.timer10ms.start(10)


    def genlayout(self):
        lay = QHBoxLayout()
        lay.addLayout(self.genlayout_main())
        lay.addWidget(self.wdgChunks)
        return lay


    def genlayout_serial_buff(self):
        lay = QHBoxLayout()
        lay.addWidget(self.wdgSerialPort)
        lay.addWidget(self.wdgBuffer)
        return lay

    def genlayout_main(self):

        lay = QVBoxLayout()
        lay.setAlignment(Qt.AlignTop)

        lay.addWidget(self.label_title)
        lay.addWidget(self.wdgAudioStat)
        lay.addWidget(self.wdgSelectFile)
        lay.addWidget(self.wdgPosition)
        lay.addLayout(self.genlayout_serial_buff())
        lay.addWidget(self.wdgOscLR)

        return lay



    def timerevent(self):

        if self.wdgSerialPort.isSerialPortOpen():
            self.ioproc()
        else:
            self.wdgSerialPort.ReopenPort()


    def stat_update(self, bufval, buff):

        self.progressBarBuffer.setValue(32-bufval)
        self.label_bsent.setText( str( int(self.sentbytes / 1024)))
        self.gfxleft.redraw(buff)
        self.gfxright.redraw(buff)

        # if buff.__len__():
        #     self.progressBarFilepos.Increment()
        #            self.progressBarFilepos.setMinimum(0)
        #            self.progressBarFilepos.setValue(0)
        #            self.progressBarFilepos.setMaximum()

    def ioproc(self):

        byte = self.serial.read_all()
        if byte.__len__() < 1:
            return

        bufval = int(byte[-1])

        if bufval < 2:
            return

        buff = self.afile.read1k()
        self.serial.write(buff)
        self.sentbytes = self.sentbytes + buff.__len__()

        # UI update 1/5 sec
        self.updateuicnt = self.updateuicnt + 1
        if self.updateuicnt < self.guirate:
            return

        self.updateuicnt = 0
        self.stat_update(bufval, buff)


    def on_file_selected(self, jcmd : Dict):

        print("File Selected", jcmd)

        filename = jcmd['open-file']

        self.afile.set_file(filename)
        self.wdgChunks.scanChunks(filename)

        self.wdgAudioStat.setParam({ 'sample-rate' : 33000 })