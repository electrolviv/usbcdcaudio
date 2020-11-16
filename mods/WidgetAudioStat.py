from typing import Dict

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QGraphicsView, QHBoxLayout, QVBoxLayout, QLabel, QFrame

from misc import picture_to_qgview


# self.label_bsent = QLabel()
# self.label_srate  = QLabel()
# self.label_channels  = QLabel()
# self.label_duration  = QLabel()


class WidgetAudioStat(QWidget):

    logo_width = 200
    logo_height = 140

    def __init__(self):

        super(WidgetAudioStat, self).__init__()

        self.graphicsViewLogo  = QGraphicsView()
        self.graphicsViewLogo.setFixedSize(self.logo_width + 2, self.logo_height + 2)

        self.graphicsViewBoard = QGraphicsView()
        self.graphicsViewBoard.setFixedSize(self.logo_width + 2, self.logo_height + 2)

        picture_to_qgview('img/elvivlogos.png', self.graphicsViewLogo, QSize(160, 48))
        picture_to_qgview('img/brd.png', self.graphicsViewBoard, QSize(self.logo_width, self.logo_height))

        # background-color: #CCC;
        self.setStyleSheet("border: 1px solid #AAA;")

        self.setMaximumHeight(self.logo_height + 16)

        self.setLayout(self.genlayout())


    def genlayout(self):

        arr = [
            'Bytes Sent',
            'Sample Rate',
            'Channels',
            'Duration' ]

        arr3 = [
            'KBytes',
            'kHz',
            'Mono',
            'sec' ]

        tmp1 = QVBoxLayout()
        tmp1.setAlignment(Qt.AlignTop)

        tmp2 = QVBoxLayout()
        tmp2.setAlignment(Qt.AlignTop)

        tmp3 = QVBoxLayout()
        tmp3.setAlignment(Qt.AlignTop)


        for txt in arr:
            lbl = QLabel(txt)
            tmp1.addWidget(lbl)

            lbl = QLabel("0")
            lbl.setMinimumWidth(60)
            lbl.setAlignment(Qt.AlignRight)
            tmp2.addWidget(lbl)

        for txt in arr3:
            tmp3.addWidget(QLabel(txt))

        tmp = QHBoxLayout()
        tmp.setAlignment(Qt.AlignTop)
        tmp.setContentsMargins(12, 4, 12, 4)
        tmp.addLayout(tmp1, 50)
        tmp.addLayout(tmp2, 25)
        tmp.addLayout(tmp3, 25)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.setContentsMargins(0, 8, 0, 4)
        lay.addWidget(self.graphicsViewLogo, 35)
        lay.addLayout(tmp, 30)
        lay.addWidget(self.graphicsViewBoard, 35)

        return lay

    def setParam(self, jparam : Dict):
        print(jparam)

        # Update File Info
        # self.label_srate.setText(    str(self.afile.handle.samplerate) )
        # self.label_channels.setText( str(self.afile.handle.channels) )
        # self.label_duration.setText( self.seconds_to_time(self.afile.handle.duration) )
