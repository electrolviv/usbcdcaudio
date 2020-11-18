from typing import Dict

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QGraphicsView, QHBoxLayout, QVBoxLayout, QLabel

from mods.misc import picture_to_qgview


# self.label_bsent = QLabel()
# self.label_srate  = QLabel()
# self.label_channels  = QLabel()
# self.label_duration  = QLabel()


class WidgetAudioStat(QWidget):

    logo_width = 200
    logo_height = 140

    arr = [ ['Bytes Sent',          'KBytes'    ],
            ['Sample Rate',         'kHz'       ],
            ['Channels',            'Mono'      ],
            ['Duration',            'sec'       ] ]

    sentbytes = 0

    def __init__(self):

        super(WidgetAudioStat, self).__init__()

        self.labels = []
        for idx in range(len(self.arr)):
            lbl = QLabel("-")
            lbl.setMinimumWidth(60)
            lbl.setAlignment(Qt.AlignRight)
            self.labels.append(lbl)


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

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.setContentsMargins(0, 8, 0, 4)
        lay.addWidget(self.graphicsViewLogo, 35)
        lay.addLayout(self.genlayout_stat(), 30)
        lay.addWidget(self.graphicsViewBoard, 35)

        return lay


    def genlayout_stat(self):

        lay = QVBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.setContentsMargins(12, 4, 12, 4)

        for idx in range(len(self.arr)):

            lbl_info = QLabel(self.arr[idx][0])
            lbl_info.setMinimumWidth(140)

            lbl_val = self.labels[idx]
            lbl_units = QLabel(self.arr[idx][1])

            tmp = QHBoxLayout()
            tmp.addWidget(lbl_info,  60)
            tmp.addWidget(lbl_val,   20)
            tmp.addWidget(lbl_units, 20)

            lay.addLayout(tmp)

        return lay

    def setParam(self, jparam : Dict):

        if 'bsent' in jparam:
            self.sentbytes = self.sentbytes + jparam['bsent']
            self.labels[0].setText(str(int(self.sentbytes / 1024)))

        elif 'sample-rate' in jparam:
            self.labels[1].setText( str(jparam['sample-rate']))

        else:
            print(jparam)
            raise ValueError

        # Update File Info
        # self.label_srate.setText(    str(self.afile.handle.samplerate) )
        # self.label_channels.setText( str(self.afile.handle.channels) )
        # self.label_duration.setText( self.seconds_to_time(self.afile.handle.duration) )
