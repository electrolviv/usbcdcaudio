import sys
import copy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPaintEvent
from PyQt5.QtWidgets import QWidget, QApplication


class WidgetOsciloscope(QWidget):

    def __init__(self):
        super().__init__()

        self.buff = [0] * 1000

        self.setMinimumSize(160, 140)

        # for i in range(1000):
        #     v = i & 255
        #     if v > 127:
        #         v -= 255
        #     self.buff.append(v)


    def paintEvent(self, event: QPaintEvent) -> None:

        w, h = self.width(), self.height()
        centery = int(h/2)
        ky = h / 255

        buff = self.buff

        qpainter = QPainter(self)  # self.pixmap

        # qpainter.setRenderHint(0)

        # Clear Screen
        qpainter.fillRect(0, 0, w, h, Qt.black)

        # Center line
        qpainter.setPen(QColor(255, 255, 255))
        qpainter.drawLine(0, centery, w, centery)

        # Draw data
        if len(buff):
            qpainter.setPen(QColor(55, 255, 55))

            pxls = len(buff) if w > len(buff) else w

            for i in range(1, pxls):

                v0 = buff[i-1] - 127
                v1 = buff[i]   - 127

                dy0 = v0 * ky
                dy1 = v1 * ky

                y0 = int(centery - dy0 )
                y1 = int(centery - dy1 )
                qpainter.drawLine(i-1, y0, i, y1)

        qpainter.end()


    def setbuff(self, buff : []) -> None:
        self.buff = copy.copy(buff)
        self.update()


if __name__ == '__main__':

    App = QApplication(sys.argv)
    wdg = WidgetOsciloscope()
    wdg.show()
    wdg.update()
    sys.exit(App.exec())
