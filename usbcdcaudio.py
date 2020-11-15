#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Deps: PyQt5
# Deps: GStreamer
# Deps: pyserial    ( $ python3 -m pip install pyserial )
# Deps: audioread   ( $ python3 -m pip install audioread )

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory
from mods.WidgetAudioPlayer import WidgetAudioPlayer

if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    app.setStyle(QStyleFactory.create('oxygen'))

    application = WidgetAudioPlayer()
    application.show()

    sys.exit(app.exec())
