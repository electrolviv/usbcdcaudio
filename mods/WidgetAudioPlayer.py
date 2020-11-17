from typing import Dict

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QFrame, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from WidgetAudioStat import WidgetAudioStat
from WidgetBuffer import WidgetBuffer
from WidgetMP3Frames import WidgetMP3Frames
from WidgetPosition import WidgetPosition
from WidgetSelectFile import WidgetSelectFile
from WidgetSerialPort import WidgetSelectSerialPort
from WidgetStereoOsc import WidgetStereoOsc

from audiofile import AudioFile


class WidgetAudioPlayer(QWidget):

    updateuicnt = 0


    def __init__(self):

        super(WidgetAudioPlayer, self).__init__()

        # Global Objects
        self.afile = AudioFile()

        # setup
        self.timerrate = 10  # ms
        self.guirate   = 3   # xtimerrate


        self.setWindowTitle("MP3-USB Audio Player")

        self.label_title = QLabel("USB CDC MP3 Audio Player")
        self.customize_ui()

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

    def customize_ui(self):
        self.label_title.setAlignment( Qt.AlignTop | Qt.AlignCenter )
        self.label_title.setFixedHeight(42)
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setFont(QFont('Arial', 14, 200, True))


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


    def stat_update(self, inbufval : int, buff : bytes) -> None:
        self.wdgAudioStat.setParam({'bsent' : len(buff)})
        self.wdgBuffer.setValue(inbufval)
        self.wdgOscLR.update_osc_data(buff)

    def ioproc(self):

        inbuff = self.wdgSerialPort.ReadSerial()

        if not inbuff:
            return

        bufval = int(inbuff[-1])
        if bufval < 2:
            return

        outbuff = self.afile.read1k()

        self.wdgSerialPort.WriteSerial(outbuff)

        # UI update 1/5 sec
        self.updateuicnt = self.updateuicnt + 1
        if self.updateuicnt < self.guirate:
            return

        self.updateuicnt = 0
        self.stat_update(bufval, outbuff)


    def on_file_selected(self, jcmd : Dict):

        print("File Selected", jcmd)

        filename = jcmd['open-file']

        self.afile.set_file(filename)
        self.wdgChunks.scanChunks(filename)

        self.wdgAudioStat.setParam({ 'sample-rate' : 33000 })