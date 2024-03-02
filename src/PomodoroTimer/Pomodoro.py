from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QLCDNumber, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import sys

timeStudy = 25
timeBreak = 10
numSecTens = 0
numSecOnes = 0
numMin = 25
currentMode = "Study"


class WidgetGallery(QDialog):
    def __init__(self):
        super(WidgetGallery, self).__init__()

        self.originalPalette = QApplication.palette()

        self.createHomeGroupBox()
        self.createSettingsGroupBox()
        self.createDigitalTimer()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.clockGroupBox)
        mainLayout.addWidget(self.homeGroupBox)
        mainLayout.addWidget(self.settingsGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Yu's Podomoro Timer")
        QApplication.setStyle(QStyleFactory.create('macos'))


    def createHomeGroupBox(self):
        self.homeGroupBox = QGroupBox("Home")

        self.startPushButton = QPushButton("Start")
        self.startPushButton.setDefault(True)

        self.stopPushButton = QPushButton("Stop")
        self.stopPushButton.setDefault(True)

        self.resetPushButton = QPushButton("Reset")
        self.resetPushButton.setDefault(True)

        self.modePushButton = QPushButton("Mode")
        self.modePushButton.setDefault(True)

        layout = QVBoxLayout()
        layout.addWidget(self.startPushButton)
        layout.addWidget(self.stopPushButton)
        layout.addWidget(self.resetPushButton)
        layout.addWidget(self.modePushButton)

        self.homeGroupBox.setLayout(layout)

    def createSettingsGroupBox(self):
        self.settingsGroupBox = QGroupBox("Settings")

        studyLabel = QLabel("Study: ")
        studySpinBox = QSpinBox()
        studySpinBox.setValue(50)

        breakLabel = QLabel("Break: ")
        breakSpinBox = QSpinBox()
        breakSpinBox.setValue(30)

        alertCheckBox = QCheckBox("Alert")
        alertCheckBox.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(studyLabel, 0, 0, 1, 1)
        layout.addWidget(studySpinBox, 0, 1, 1, 2)
        layout.addWidget(breakLabel, 1, 0, 1, 1)
        layout.addWidget(breakSpinBox, 1, 1, 1, 2)
        layout.addWidget(alertCheckBox, 2, 0)

        self.settingsGroupBox.setLayout(layout)









if __name__ == "__main__":

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())