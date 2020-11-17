from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QProgressBar


# if buff.__len__():
#     self.progressBarFilepos.Increment()


class WidgetBuffer(QWidget):

    def __init__(self):

        super(WidgetBuffer, self).__init__()

        self.gbox = QGroupBox("Hardware Buffer")

        self.progressBarBuffer = QProgressBar()

        self.setLayout(self.genlayout())


    def genlayout(self):

        self.gbox.setLayout(self.genlayout_gbox())

        lay = QVBoxLayout()
        lay.addWidget(self.gbox)
        return lay


    def genlayout_gbox(self):
        lay = QVBoxLayout()
        lay.addWidget(self.progressBarBuffer)
        return lay

    def setValue(self, val : int) -> None:
        self.progressBarBuffer.setValue(32 - val)

