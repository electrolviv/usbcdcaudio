from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView


class Gfxosc:

    def __init__(self, graphicsview : QGraphicsView):
        self.gv = graphicsview
        self.w, self.h = graphicsview.width() - 2, graphicsview.height() - 2
        self.pixmap = QPixmap(self.w, self.h)

    def redraw(self, buff):

        qpainter = QPainter(self.pixmap)
        qpainter.setRenderHint(0)

        # Clear Screen
        qpainter.fillRect(0, 0, self.pixmap.width(), self.pixmap.height(), Qt.black)

        # Draw data
        qpainter.setPen(QColor(255, 255, 255))

        centery = self.h/2
        qpainter.drawLine(0, centery, self.w, centery)

        if buff.__len__():
            qpainter.setPen(QColor(55, 255, 55))

            for i in range(1, self.w - 1):
                y0 = centery - ((128 - buff[i-1]) / 3)
                y1 = centery - ((128 - buff[i]  ) / 3)
                qpainter.drawLine(i-1, y0, i, y1)

        qpainter.end()

        # Pixmap to QGraphicsView
        scene = QGraphicsScene()
        scene.addPixmap(self.pixmap)
        self.gv.setRenderHint(0)
        self.gv.setScene(scene)
