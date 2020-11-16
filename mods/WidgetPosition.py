from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QGroupBox


class WidgetPosition(QWidget):

    def __init__(self):
        super(WidgetPosition, self).__init__()
        self.gbox = QGroupBox("Position")
        self.horizontalSliderPos = QSlider(Qt.Horizontal)
        self.setLayout(self.genlayout())


    def genlayout(self):
        self.gbox.setLayout(self.genlayout_gbox())

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(self.gbox)
        return lay

    def genlayout_gbox(self):
        lay = QHBoxLayout()
        lay.addWidget(self.horizontalSliderPos)
        return lay
