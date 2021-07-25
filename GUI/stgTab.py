import os
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QFileDialog, QGroupBox, QComboBox

from .config import configHelper, stagePositions
from .styleSheet import invalid_stylesheet, valid_stylesheet, zero_button_stylesheet, left_button_stylesheet, right_button_stylesheet


class stgTab(QWidget):
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.config = configHelper()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.optionsLayout = QGridLayout()
        self.optionsLayout.addWidget(QLabel("Series name"), 0, 0)
        self.seriesNameLineEdit = QLineEdit("")
        self.seriesNameLineEdit.setPlaceholderText("Series name")
        self.optionsLayout.addWidget(self.seriesNameLineEdit, 0, 1)
        self.layout.addLayout(self.optionsLayout)

        self.gridButtonsLayout = QHBoxLayout()
        self.offsetWidget = toggleButtonWidget("Defined offset", "Percentage overlap")
        self.gridButtonsLayout.addWidget(self.offsetWidget)
        self.snakeWidget = toggleButtonWidget("Snake along row", "Row by row")
        self.gridButtonsLayout.addWidget(self.snakeWidget)
        self.layout.addLayout(self.gridButtonsLayout)

        self.createGridOptionLayout()
        self.layout.addWidget(self.gridTypeOptions)

        # --- positions group --- #
        self.gridGroup = QGroupBox("Positions")
        self.posLayout = QGridLayout()
        self.labelsLayout = QHBoxLayout()
        for label in ['X position', 'Y position', 'Z1 position']:
            labelWidget = QLabel(label)
            labelWidget.setAlignment(Qt.AlignCenter)
            self.labelsLayout.addWidget(labelWidget, 2)

        # Auto focus offset
        labelLayout = QHBoxLayout()
        labelLayout.addStretch()
        labelWidget = QLabel('Auto focus offset')
        labelWidget.setAlignment(Qt.AlignLeft)
        labelLayout.addWidget(labelWidget)
        self.zeroAFButton = QPushButton("Zero")
        self.zeroAFButton.setStyleSheet(zero_button_stylesheet)
        self.zeroAFButton.setFixedSize(40, 20)
        labelLayout.addWidget(self.zeroAFButton)
        labelLayout.addStretch()
        self.labelsLayout.addLayout(labelLayout, 2)

        labelLayout = QHBoxLayout()
        labelLayout.addStretch()
        labelWidget = QLabel('Z2 position')
        labelWidget.setAlignment(Qt.AlignLeft)
        labelLayout.addWidget(labelWidget)
        self.zeroZ2Button = QPushButton("Zero")
        self.zeroZ2Button.setStyleSheet(zero_button_stylesheet)
        self.zeroZ2Button.setFixedSize(40, 20)
        labelLayout.addWidget(self.zeroZ2Button)
        labelLayout.addStretch()
        self.labelsLayout.addLayout(labelLayout, 2)

        self.posLayout.addLayout(self.labelsLayout, 0, 1)

        self.posLayout.addWidget(QLabel("Initial position"), 1, 0)
        self.initialPosWidget = inputWidget()
        self.posLayout.addWidget(self.initialPosWidget, 1, 1)
        self.posLayout.addWidget(QLabel("Position along X"), 2, 0)
        self.alongXWidget = inputWidget()
        self.posLayout.addWidget(self.alongXWidget, 2, 1)
        self.posLayout.addWidget(QLabel("Position along Y"), 3, 0)
        self.alongYWidget = inputWidget()
        self.posLayout.addWidget(self.alongYWidget, 3, 1)

        self.gridGroup.setLayout(self.posLayout)
        self.layout.addWidget(self.gridGroup)

        self.layout.addStretch()

        self.buttons = QHBoxLayout()
        self.loadSTGButton = QPushButton("Load position from file")
        self.buttons.addWidget(self.loadSTGButton)
        self.generateSTGButton = QPushButton("Generate STG file")
        self.buttons.addWidget(self.generateSTGButton)
        self.layout.addLayout(self.buttons)

        self.loadSTGButton.clicked.connect(self.onLoadSTGButtonClicked)
        self.generateSTGButton.clicked.connect(self.onGenerateSTGButtonClicked)
        self.zeroAFButton.clicked.connect(self.onZeroAFButtonClicked)
        self.zeroZ2Button.clicked.connect(self.onZeroZ2ButtonClicked)

        self.initialPosWidget.messageSignal.connect(self.passMessageSignal)
        self.alongXWidget.messageSignal.connect(self.passMessageSignal)
        self.alongYWidget.messageSignal.connect(self.passMessageSignal)

        self.offsetWidget.changeSignal.connect(self.onOffsetChange)

    def createGridOptionLayout(self):
        # --- grid type group --- #
        self.gridTypeOptions = QGroupBox("Grid options")
        self.gridTypeLayout = QVBoxLayout()

        self.stageGridLayout = QHBoxLayout()
        self.stageGridLayout.addWidget(QLabel("No. of rows"))
        self.numRowLineEdit = QLineEdit(str(self.config.num_rows))
        self.numRowLineEdit.setPlaceholderText("Number of rows")
        self.stageGridLayout.addWidget(self.numRowLineEdit)
        self.stageGridLayout.addWidget(QLabel("No. of cols"))
        self.numColLineEdit = QLineEdit(str(self.config.num_cols))
        self.numColLineEdit.setPlaceholderText("Number of columns")
        self.stageGridLayout.addWidget(self.numColLineEdit)
        self.gridTypeLayout.addLayout(self.stageGridLayout)

        self.offsetLayout = QHBoxLayout()
        self.offsetLayout.addWidget(QLabel("X offset (um)"))
        self.xdirOffsetLineEdit = QLineEdit(str(self.config.x_dir_offset))
        self.xdirOffsetLineEdit.setPlaceholderText("X offset between positions (horizontal direction)")
        self.offsetLayout.addWidget(self.xdirOffsetLineEdit)

        self.offsetLayout.addWidget(QLabel("Y offset (um)"))
        self.ydirOffsetLineEdit = QLineEdit(str(self.config.y_dir_offset))
        self.ydirOffsetLineEdit.setPlaceholderText("Y offset between positions(vertical direction)")
        self.offsetLayout.addWidget(self.ydirOffsetLineEdit)

        self.offsetLayout.addWidget(QLabel("Row offset (um)"))
        self.rowOffsetLineEdit = QLineEdit(str(self.config.row_offset))
        self.rowOffsetLineEdit.setPlaceholderText("Offset (x direction) between rows")
        self.offsetLayout.addWidget(self.rowOffsetLineEdit)

        self.offsetLayout.addWidget(QLabel("Row count offset"))
        self.rowCountOffsetLineEdit = QLineEdit(str(self.config.row_count_offset))
        self.rowCountOffsetLineEdit.setPlaceholderText("Offset number of columns for alternate rows")
        self.offsetLayout.addWidget(self.rowCountOffsetLineEdit)

        self.gridTypeLayout.addLayout(self.offsetLayout)
        self.gridTypeOptions.setLayout(self.gridTypeLayout)

    def createGridOptionLayout_2(self):
        # --- grid type group --- #
        self.gridTypeOptions = QGroupBox("Grid options")
        self.gridTypeLayout = QVBoxLayout()

        self.stageGridLayout = QHBoxLayout()
        self.stageGridLayout.addWidget(QLabel("No. of rows"))
        self.numRowLineEdit = QLineEdit(str(self.config.num_rows))
        self.numRowLineEdit.setPlaceholderText("Number of rows")
        self.stageGridLayout.addWidget(self.numRowLineEdit)
        self.stageGridLayout.addWidget(QLabel("No. of cols"))
        self.numColLineEdit = QLineEdit(str(self.config.num_cols))
        self.numColLineEdit.setPlaceholderText("Number of columns")
        self.stageGridLayout.addWidget(self.numColLineEdit)
        self.gridTypeLayout.addLayout(self.stageGridLayout)

        self.offsetLayout = QHBoxLayout()
        self.offsetLayout.addWidget(QLabel("X percentage overlap (%)"))
        self.xperOverlapLineedit = QLineEdit(str(self.config.x_per_overlap))
        self.xperOverlapLineedit.setPlaceholderText("X percentage offset between positions (horizontal direction)")
        self.offsetLayout.addWidget(self.xperOverlapLineedit)

        self.offsetLayout.addWidget(QLabel("Y percentage overlap (%)"))
        self.yperOverlapLineEdit = QLineEdit(str(self.config.y_per_overlap))
        self.yperOverlapLineEdit.setPlaceholderText("Y offset between positions(vertical direction)")
        self.offsetLayout.addWidget(self.yperOverlapLineEdit)
        self.gridTypeLayout.addLayout(self.offsetLayout)

        # camera layout
        self.cameraLayout = QHBoxLayout()
        self.magnificationLabel = QLabel("Magnification")
        self.cameraLayout.addWidget(self.magnificationLabel)
        self.magnificationComboBox = QComboBox()
        self.magnificationComboBox.addItems(["10x", "20x", "40x", "60x", "100x"])
        self.magnificationComboBox.setEditable(True)
        self.cameraLayout.addWidget(self.magnificationComboBox)

        self.cameraLabel = QLabel("Camera")
        self.cameraLayout.addWidget(self.cameraLabel)
        self.cameraComboBox = QComboBox()
        self.cameraComboBox.addItems(["Prime 95B", "Orca Fusion", "Orca Flash", "CoolSNAP EZ", "Custom"])
        self.cameraLayout.addWidget(self.cameraComboBox)

        self.cameraHeightLabel = QLabel("Camera height")
        self.cameraLayout.addWidget(self.cameraHeightLabel)
        self.cameraHeightLineEdit = QLineEdit(str(self.config.height))
        self.cameraLayout.addWidget(self.cameraHeightLineEdit)

        self.cameraWidthLabel = QLabel("Camera width")
        self.cameraLayout.addWidget(self.cameraWidthLabel)
        self.cameraWidthLineEdit = QLineEdit(str(self.config.width))
        self.cameraLayout.addWidget(self.cameraWidthLineEdit)

        self.cameraPixelSizeLabel = QLabel("Pixel size")
        self.cameraLayout.addWidget(self.cameraPixelSizeLabel)
        self.cameraPixelSizeLineEdit = QLineEdit(str(self.config.pixel_size))
        self.cameraLayout.addWidget(self.cameraPixelSizeLineEdit)

        self.gridTypeLayout.addLayout(self.cameraLayout)

        self.gridTypeOptions.setLayout(self.gridTypeLayout)

        self.cameraComboBox.currentTextChanged.connect(self.onCameraChange)

    @pyqtSlot(str, str)
    def passMessageSignal(self, msg, msg_type):
        self.messageSignal.emit(msg, msg_type)

    @pyqtSlot()
    def onOffsetChange(self):
        option = self.offsetWidget.options_index
        self.layout.removeWidget(self.gridTypeOptions)
        self.gridTypeOptions.close()

        if option == 0:
            self.createGridOptionLayout()
        elif option == 1:
            self.createGridOptionLayout_2()

        self.layout.insertWidget(2, self.gridTypeOptions)
        self.layout.update()

    def onCameraChange(self):
        camera = self.cameraComboBox.currentText()
        if camera == "Custom":
            pass
        else:
            self.config.camera = self.config.available_cameras[camera]

            self.config.height = self.cameraHeightLineEdit.setText(str(self.config.camera.height))
            self.config.width = self.cameraWidthLineEdit.setText(str(self.config.camera.width))
            self.config.pixel_size = self.cameraPixelSizeLineEdit.setText(str(self.config.camera.pixel_size))

    def onZeroAFButtonClicked(self):
        widget_list = [self.initialPosWidget, self.alongXWidget, self.alongYWidget]
        for pos_widget in widget_list:
            pos_widget.zeroAFOffset()
        self.messageSignal.emit("Auto focus offset zeroed.", "info")

    def onZeroZ2ButtonClicked(self):
        widget_list = [self.initialPosWidget, self.alongXWidget, self.alongYWidget]
        for pos_widget in widget_list:
            pos_widget.zeroZ2Offset()
        self.messageSignal.emit("Z2 position zeroed.", "info")

    def onLoadSTGButtonClicked(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Choose STG file", self.config.path, filter="STG file (*.stg)")

        if os.path.isfile(filepath) is False:
            self.messageSignal.emit("No STG file was loaded.", "error")
        else:
            self.config.path = os.path.dirname(filepath)
            self.loadSTG(filepath)

            if self.config.top_left is not None:
                self.initialPosWidget.updateValues(self.config.top_left)
            if self.config.top_right is not None:
                self.alongXWidget.updateValues(self.config.top_right)
            if self.config.bottom_left is not None:
                self.alongYWidget.updateValues(self.config.bottom_left)

            self.messageSignal.emit(f"STG file loaded from '{filepath}'", "info")

    def loadSTG(self, file):
        # TODO: ensure stg_file is valid
        stg_file = np.genfromtxt(file, skip_header=4, dtype='object', delimiter=', ')
        if stg_file.shape[0] != 3:
            self.messageSignal.emit("Please ensure that the STG file has only 3 positions", "error")
        else:
            self.config.top_left = stagePositions(*stg_file[0, 1:6].astype(float))
            self.config.top_right = stagePositions(*stg_file[1, 1:6].astype(float))
            self.config.bottom_left = stagePositions(*stg_file[2, 1:6].astype(float))

    def onGenerateSTGButtonClicked(self):
        positions = []
        stg_positions = []
        save_pass = True

        widget_list = [self.initialPosWidget, self.alongXWidget, self.alongYWidget]
        for pos_widget in widget_list:
            pos = pos_widget.getValues()
            if pos is not None:
                positions.append(pos)
            else:
                save_pass = False

        if save_pass:
            series_name = self.seriesNameLineEdit.text()

            self.config.num_rows = int(self.numRowLineEdit.text())
            self.config.num_cols = int(self.numColLineEdit.text())

            is_snake = True if self.snakeWidget.options_index == 0 else False

            if positions[0][2] == positions[0][4]:
                is_same_z2 = True
            else:
                is_same_z2 = False

            if self.offsetWidget.options_index == 0:
                self.config.x_dir_offset = float(self.xdirOffsetLineEdit.text())
                self.config.y_dir_offset = float(self.ydirOffsetLineEdit.text())
                self.config.row_offset = float(self.rowOffsetLineEdit.text())
                self.config.row_count_offset = int(self.rowCountOffsetLineEdit.text())

                stg_positions = self.generatePositions(series_name, positions, self.config.num_rows, self.config.num_cols,
                                                       self.config.x_dir_offset, self.config.y_dir_offset,
                                                       is_same_z2=is_same_z2, row_offset=self.config.row_offset,
                                                       row_count_offset=self.config.row_count_offset, is_snake=is_snake
                                                       )
            elif self.offsetWidget.options_index == 1:
                self.config.x_per_overlap = float(self.xperOverlapLineedit.text())
                self.config.y_per_overlap = float(self.yperOverlapLineEdit.text())
                self.config.height = float(self.cameraHeightLineEdit.text())
                self.config.width = float(self.cameraWidthLineEdit.text())
                self.config.pixel_size = float(self.cameraPixelSizeLineEdit.text())
                self.config.magnification = float(self.magnificationComboBox.currentText().rstrip('xX'))

                pixel2um = self.config.pixel_size/self.config.magnification
                x_offset = self.config.width * (1 - self.config.x_per_overlap / 100) * pixel2um
                y_offset = self.config.height * (1 - self.config.y_per_overlap / 100) * pixel2um

                stg_positions = self.generatePositions(series_name, positions, self.config.num_rows, self.config.num_cols,
                                                       x_offset, y_offset, is_same_z2=is_same_z2, is_snake=is_snake)

            self.config.stg_positions = stg_positions
            filepath, _ = QFileDialog.getSaveFileName(self, "Save STG file to", filter="STG file (*.stg);;")
            self.saveSTG(filepath, stg_positions)
        else:
            self.messageSignal.emit("STG file has not been saved.", "error")

    def generatePositions(self, series_name, positions, rows, cols, x_offset, y_offset,
                          is_same_z2=False, row_offset=0.0, row_count_offset=0, is_snake=True):
        initial_pos = positions[0][:3]
        pos_along_x = positions[1][:3]
        pos_along_y = positions[2][:3]

        vec_x = np.subtract(pos_along_x, initial_pos)
        unit_vec_x = vec_x / np.sqrt(np.dot(vec_x, vec_x))
        af_offset_x = (positions[1][3] - positions[0][3]) / np.sqrt(np.dot(vec_x, vec_x))

        vec_y = np.subtract(pos_along_y, initial_pos)
        unit_vec_y = vec_y / np.sqrt(np.dot(vec_y, vec_y))
        af_offset_y = (positions[2][3] - positions[0][3]) / np.sqrt(np.dot(vec_x, vec_x))

        stg_positions = np.empty(rows * cols + rows//2*row_count_offset, dtype="object")

        current_pos = np.array(initial_pos)
        current_af = positions[0][3]
        x_movement_dir = 1
        count = 0
        for row in range(rows):
            num_cols = cols + (row % 2) * row_count_offset
            for col in range(num_cols):
                line = [f"{series_name}_{row},{col}"]
                current_pos = current_pos + (x_movement_dir * unit_vec_x * x_offset * (col > 0))
                current_af = current_af + (x_movement_dir * af_offset_x * x_offset * (col > 0))
                line.extend(list(current_pos.round(2)))
                line.append(current_af.round(2))
                line.append(current_pos[2].round(2) if is_same_z2 else 0.0)
                stg_positions[count] = line
                count += 1
            if is_snake:
                x_movement_dir = -x_movement_dir
                current_pos = current_pos + (unit_vec_y * y_offset) + (
                            x_movement_dir * np.abs(row_offset) * row_count_offset * unit_vec_x)
                current_af = current_af + (af_offset_y * y_offset) + (
                            x_movement_dir * np.abs(row_offset) * row_count_offset * af_offset_x)
            else:
                current_pos = current_pos + (unit_vec_y * y_offset) \
                              + (x_movement_dir * np.abs(row_offset) * row_count_offset * unit_vec_x) \
                              - x_movement_dir * unit_vec_x * x_offset * (cols + ((row + 1) % 2) * row_count_offset - 1)
                current_af = current_af + (af_offset_y * y_offset) \
                             + (x_movement_dir * np.abs(row_offset) * row_count_offset * af_offset_x)\
                             - x_movement_dir * af_offset_x * x_offset * (cols + ((row + 1) % 2) * row_count_offset - 1)

        return stg_positions

    def saveSTG(self, file, positions):
        header = f'"Stage Memory List", Version 6.0\n ' \
                 f'0, 0, 0, 0, 0, 0, 0, "microns", "microns"\n ' \
                 f'0\n' \
                 f'{positions.shape[0]}\n'
        with open(file, 'w') as text:
            text.writelines(header)
            for pos in positions:
                text.writelines(
                    f'"{pos[0]}", {pos[1]}, {pos[2]}, {pos[3]}, {pos[4]}, {pos[5]}, '
                    f'FALSE, -9999, TRUE, TRUE, 0, -1, ""\n')

        dirname, basename = os.path.split(file)
        self.messageSignal.emit(f"STG file saved as {basename} to '{dirname}'", "info")


class toggleButtonWidget(QWidget):
    changeSignal = pyqtSignal()

    def __init__(self, left_name, right_name):
        super(QWidget, self).__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.options_index = 0

        self.leftButton = QPushButton(left_name)
        self.leftButton.setStyleSheet(left_button_stylesheet)
        self.leftButton.setProperty("type", 1)
        self.leftButton.style().unpolish(self.leftButton)
        self.leftButton.style().polish(self.leftButton)
        self.layout.addWidget(self.leftButton)

        self.rightButton = QPushButton(right_name)
        self.rightButton.setStyleSheet(right_button_stylesheet)
        self.rightButton.setProperty("type", 0)
        self.rightButton.style().unpolish(self.rightButton)
        self.rightButton.style().polish(self.rightButton)
        self.layout.addWidget(self.rightButton)
        self.setLayout(self.layout)

        self.leftButton.clicked.connect(self.onLeftButtonClicked)
        self.rightButton.clicked.connect(self.onRightButtonClicked)

    def onLeftButtonClicked(self):
        self.options_index = 0
        self.leftButton.setProperty("type", 1)
        self.leftButton.style().unpolish(self.leftButton)
        self.leftButton.style().polish(self.leftButton)
        self.rightButton.setProperty("type", 0)
        self.rightButton.style().unpolish(self.rightButton)
        self.rightButton.style().polish(self.rightButton)
        self.changeSignal.emit()

    def onRightButtonClicked(self):
        self.options_index = 1
        self.leftButton.setProperty("type", 0)
        self.leftButton.style().unpolish(self.leftButton)
        self.leftButton.style().polish(self.leftButton)
        self.rightButton.setProperty("type", 1)
        self.rightButton.style().unpolish(self.rightButton)
        self.rightButton.style().polish(self.rightButton)
        self.changeSignal.emit()


class inputWidget(QWidget):
    messageSignal = pyqtSignal(str, str)

    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QHBoxLayout()
        self.xLineEdit = QLineEdit("")
        self.yLineEdit = QLineEdit("")
        self.z1LineEdit = QLineEdit("")
        self.afLineEdit = QLineEdit("")
        self.z2LineEdit = QLineEdit("")
        self.inputs = [self.xLineEdit, self.yLineEdit, self.z1LineEdit, self.afLineEdit, self.z2LineEdit]
        for input in self.inputs:
            self.layout.addWidget(input)

        self.setLayout(self.layout)

    def updateValues(self, pos):
        self.xLineEdit.setText(str(pos.x))
        self.yLineEdit.setText(str(pos.y))
        self.z1LineEdit.setText(str(pos.z1))
        self.afLineEdit.setText(str(pos.af))
        self.z2LineEdit.setText(str(pos.z2))

    def getValues(self):
        is_valid = True
        for line_edit in self.inputs:
            is_valid = is_valid and self.validateValues(line_edit)

        if is_valid:
            values = []
            for line_edit in self.inputs:
                values.append(float(line_edit.text()))
            return values
        else:
            return None

    def validateValues(self, line_edit):
        try:
            float(line_edit.text())
            line_edit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            line_edit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Invalid configuration found. Please check the inputs.", "error")
            return False

    def zeroAFOffset(self):
        self.afLineEdit.setText("0.0")


    def zeroZ2Offset(self):
        self.z2LineEdit.setText("0.0")
