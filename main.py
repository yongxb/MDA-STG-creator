import re
import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser, QWidget, \
    QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from GUI.styleSheet import qss
from GUI.XStream import XStream, XStreamError
from GUI.aboutTab import aboutTab
from GUI.stgTab import stgTab


class stgCreatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'MultiDimensional Acquisition STG Creator'
        self.left = 100
        self.top = 100
        self.width = 1100
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = tabWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class dropShadow():
    def __init__(self, radius=10, xoffset=2, yoffset=2):
        self.color = Qt.gray
        self.radius = radius
        self.xoffset = xoffset
        self.yoffset = yoffset

    def effect(self):
        dropShadowEffect = QGraphicsDropShadowEffect()
        dropShadowEffect.setColor(self.color)
        dropShadowEffect.setBlurRadius(self.radius)
        dropShadowEffect.setXOffset(self.xoffset)
        dropShadowEffect.setYOffset(self.yoffset)

        return dropShadowEffect


class tabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.aboutTab = aboutTab(self)
        self.stgTab = stgTab(self)

        # Add tabs
        self.tabs.addTab(self.stgTab, "STG creator")
        self.tabs.addTab(self.aboutTab, "About")

        # Add tabs to widget
        self.tabs.setGraphicsEffect(dropShadow().effect())
        self.layout.addWidget(self.tabs, 3)

        self.consoleLayout = QVBoxLayout()
        self.consoleLayout.setSpacing(0)

        self.consoleHeaderLayout = QHBoxLayout()
        self.consoleLabel = QLabel("Console output")
        self.consoleLabel.setStyleSheet("QLabel{"
                                        "background: #20639B;"
                                        "color: white;"
                                        "margin: 0 7 0 7px;"
                                        "padding: 7px;"
                                        "border: 0px solid transparent;"
                                        "border-bottom: 0px solid transparent;"
                                        "border-top-left-radius: 7px;"
                                        "border-top-right-radius: 7px;"
                                        "font: bold"
                                        "}")
        self.consoleHeaderLayout.addWidget(self.consoleLabel, 10)
        self.consoleLayout.addLayout(self.consoleHeaderLayout)

        self.console = QTextBrowser(self)
        self.console.setOpenExternalLinks(True)
        self.console.setGraphicsEffect(dropShadow().effect())
        self.consoleLayout.addWidget(self.console)

        self.layout.addLayout(self.consoleLayout, 2)

        # create connections
        XStream.stdout().messageWritten.connect(self.updateConsole)
        XStreamError.stderr().errorWritten.connect(self.updateConsoleError)

        self.stgTab.messageSignal.connect(self.updateConsoleSignal)

        self.setLayout(self.layout)


    @pyqtSlot(str)
    def updateConsole(self, text):
        self.updateConsoleSignal(text.rstrip("\r\n"), "info")

    @pyqtSlot(str)
    def updateConsoleError(self, text):
        self.updateConsoleSignal(text, "error")

    @pyqtSlot(str, str)
    def updateConsoleSignal(self, text, signal_type):
        self.console.moveCursor(QTextCursor.End)
        if signal_type == "error":
            color = "191, 43, 86"
        elif signal_type == "warn":
            color = "226, 112, 0"
        elif signal_type == "load":
            color = "37, 112, 88"
        elif signal_type == "param":
            color = "40, 114, 143"
        else:
            signal_type = "info"
            color = "0, 0, 0"

        # catch folders and add hyperlink
        text = text.replace('\\', '/')
        if ":/" in text:
            pattern = re.compile(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''')
            parts = pattern.split(text)
            text = ""
            for part in parts:
                if ":/" in part:
                    text += f"<a href={part}>{part}</a>"
                else:
                    text += part
        date = datetime.now().strftime("%x %X")
        self.console.insertHtml(f"<span style=\"color:rgb({color})\">  [{date} | {signal_type}] {text}</span><br>")
        self.console.moveCursor(QTextCursor.End)
        self.console.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)

    gui = stgCreatorGUI()
    sys.exit(app.exec_())

# to run as a shortcut, create a shortcut using these options
# %systemroot%\System32\cmd.exe /c "python C:\Users\MyUsername\Documents\MyScript.py"
# C:\Users\MyUsername\Documents\
if __name__ == '__main__':
    main()

