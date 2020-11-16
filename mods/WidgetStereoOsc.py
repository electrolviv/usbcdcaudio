from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from WidgetOsc import WidgetOsciloscope


class WidgetStereoOsc(QWidget):

    def __init__(self):

        super().__init__()

        self.wdgOscL = WidgetOsciloscope()
        self.wdgOscR = WidgetOsciloscope()
        self.setMinimumHeight(128)
        self.setMaximumHeight(256)

        self.setLayout(self.genlayout())


    def genlayout(self):
        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(self.wdgOscL)
        lay.addWidget(self.wdgOscR)
        return lay
