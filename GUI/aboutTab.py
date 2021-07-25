from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, \
    QVBoxLayout, QGroupBox

from os import path


class aboutTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.versionLabel = QLabel("Multidimensional Acquisition STG creator 0.1")
        self.optionsLayout.addWidget(self.versionLabel)

        self.layout.addLayout(self.optionsLayout)
        self.layout.addStretch()