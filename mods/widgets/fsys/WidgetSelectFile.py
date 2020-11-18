import os
from typing import Callable, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QFileDialog, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


class WidgetSelectFile(QWidget):

    def __init__(self, callback : Callable[[Dict], None]):

        super(WidgetSelectFile, self).__init__()

        self.callback = callback

        self.gbox = QGroupBox("Select MP3 File")

        self.labelFileName = QLabel("-")

        self.pushButtonSelectfile = QPushButton("...")
        self.pushButtonSelectfile.setMaximumWidth(64)
        self.pushButtonSelectfile.clicked.connect(self.select_file)

        self.setLayout(self.genlayout())


    def genlayout(self):

        self.gbox.setLayout(self.genlayout_gbox())

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(self.gbox)
        return lay


    def genlayout_gbox(self):
        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(self.labelFileName)
        lay.addWidget(self.pushButtonSelectfile)
        return lay

    def update_file_props(self, filename):
        self.labelFileName.setText(os.path.basename(filename))


    def select_file(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        caption = "QFileDialog.getOpenFileName()"
        mask = "MP3 Files (*.mp3);; (*.*)"
        filename, _ = QFileDialog.getOpenFileName(self, caption, "", mask, options=options)

        if not filename:
            return

        self.update_file_props(filename)
        self.callback( { 'open-file' : filename })
