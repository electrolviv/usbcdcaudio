import os
import platform
import serial

from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QProgressBar, QPushButton, QLineEdit, QSlider, QFileDialog
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from mods.audiofile import AudioFile
from mods.gfxosc import Gfxosc


class WidgetAudioPlayer(QtWidgets.QMainWindow):

    def __init__(self):

        super(WidgetAudioPlayer, self).__init__()

        # Global Objects
        self.afile = AudioFile()
        self.serial = serial.Serial()

        # setup
        self.timerrate = 10  # ms
        self.guirate   = 3   # xtimerrate

        # Initialize UI Objects
        self.labelFileName = QLabel()
        self.progressBarBuffer = QProgressBar()
        self.pushButtonSelectfile = QPushButton()
        self.pushButtonReconnect  = QPushButton()
        self.graphicsViewLogo  = QGraphicsView()
        self.graphicsViewBoard = QGraphicsView()
        self.lineEditComport = QLineEdit()
        self.label_bsent = QLabel()
        self.label_srate  = QLabel()
        self.label_channels  = QLabel()
        self.label_duration  = QLabel()
        self.horizontalSliderPos = QSlider()

        self.updateuicnt = 0
        self.sentbytes   = 0

        # Load UI
        uic.loadUi('mods/mainwindow.ui', self)

        self.setWindowTitle("MP3-USB Audio Player")

        self.gfxleft  = Gfxosc(self.graphicsViewLeft)
        self.gfxright = Gfxosc(self.graphicsViewRight)

        self.picture_to_qgview('img/elvivlogos.png', self.graphicsViewLogo, QSize(160, 48))
        self.picture_to_qgview('img/brd.png', self.graphicsViewBoard, QSize(199, 119))

        self.pushButtonSelectfile.clicked.connect(self.select_file)


        self.timer10ms = QtCore.QTimer(self)
        self.timer10ms.timeout.connect(self.timerevent)
        self.timer10ms.setSingleShot(False)
        self.timer10ms.start(10)


    @staticmethod
    def picture_to_qgview(fname : str, qgv : QGraphicsView, ssize : QSize) -> None:
        pixmapscaled = QPixmap(fname).scaled(ssize, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        scene = QGraphicsScene()
        scene.addPixmap(pixmapscaled)
        qgv.setScene(scene)

    @staticmethod
    def seconds_to_time(s):
        secs = int(s)
        hours = int(secs / 3600)
        secs = secs - (hours * 3600)
        mins  = int(secs / 60)
        secs = secs - (mins * 60)
        r = '{0:02d}'.format(hours) + ':' + '{0:02d}'.format(mins) + ':' + '{0:02d}'.format(secs)
        return r


    def update_file_props(self, filename):
        self.labelFileName.setText(os.path.basename(filename))

    def timerevent(self):

        if self.serial.isOpen():
            self.ioproc()
        else:

            try:
                port = "COM4" if platform.system() == "Windows" else "/dev/ttyACM1"
                baudrate = 1000000
                self.serial = serial.Serial(port, baudrate)
                print("Opened")

            except serial.serialutil.SerialException:
                pass


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


    def select_file(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        caption = "QFileDialog.getOpenFileName()"
        mask = "MP3 Files (*.mp3);; (*.*)"
        filename, _ = QFileDialog.getOpenFileName(self, caption, "", mask, options=options)

        if not filename:
            return

        self.update_file_props(filename)
        self.afile.set_file(filename)

        # Update File Info
        self.label_srate.setText(    str(self.afile.handle.samplerate) )
        self.label_channels.setText( str(self.afile.handle.channels) )
        self.label_duration.setText( self.seconds_to_time(self.afile.handle.duration) )
