import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTreeWidget, QTreeWidgetItem


class WidgetMP3Frames(QWidget):

    def __init__(self):
        super(WidgetMP3Frames, self).__init__()

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabel("Offset")

        self.gbox = QGroupBox("MP3 Frames")
        self.gbox.setMaximumWidth(100)
        self.gbox.setLayout(self.genlayout_gbox())

        self.chunks = []

        self.setLayout(self.genlayout())


    def genlayout(self):
        lay = QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.gbox)
        return lay

    def genlayout_gbox(self):
        lay = QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.treeWidget)
        return lay


    def setupWidget(self):

        self.treeWidget.clear()

        for offset in self.chunks:
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, "%.X" % offset)
            self.treeWidget.addTopLevelItem(item)


    def scanChunks(self, fname : str) -> {}:
        self.chunks = []

        f = open(fname, "rb")
        fsize = os.fstat(f.fileno()).st_size
        offset = 0
        flagFirst = False

        # Scan all chunks
        while offset < fsize:

            bval = f.read(1)
            val = int(bval[0])

            if flagFirst:
                # if (val >> 5) == 7:
                if val == 0xFB:
                    self.chunks.append(offset-1)
                flagFirst = False

            if not flagFirst:
                if val == 0xFF:
                    flagFirst = True

            offset += 1

        # Filter invalid
        for idx in range(len(self.chunks)-1):
            offs1 = self.chunks[idx]
            offs2 = self.chunks[idx+1]

            print("%X:%X  %i" % (offs1, offs2, offs2 - offs1) )

        self.setupWidget()

        return {}
