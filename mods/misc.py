from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


def picture_to_qgview(fname: str, qgv: QGraphicsView, ssize: QSize) -> None:
    pixmapscaled = QPixmap(fname).scaled(ssize, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
    scene = QGraphicsScene()
    scene.addPixmap(pixmapscaled)
    qgv.setScene(scene)


def seconds_to_time(s):
    secs = int(s)
    hours = int(secs / 3600)
    secs = secs - (hours * 3600)
    mins  = int(secs / 60)
    secs = secs - (mins * 60)
    r = '{0:02d}'.format(hours) + ':' + '{0:02d}'.format(mins) + ':' + '{0:02d}'.format(secs)
    return r


# self.setFrameShape(QFrame.Box)
# self.setFrameShadow(QFrame.Raised)
