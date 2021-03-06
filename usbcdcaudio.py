#!/usr/bin/python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":

    import sys
    from PyQt5 import QtWidgets
    from PyQt5.QtWidgets import QStyleFactory

    sys.path.append('mods')
    sys.path.append('mods/gui')
    sys.path.append('mods/widgets')
    sys.path.append('mods/widgets/audio')
    sys.path.append('mods/widgets/fsys')
    sys.path.append('mods/widgets/periph')

    from WidgetAudioPlayer import WidgetAudioPlayer


    app = QtWidgets.QApplication([])
    app.setStyle(QStyleFactory.create('oxygen'))

    application = WidgetAudioPlayer()
    application.show()

    sys.exit(app.exec())
