# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

from clickableqlabel import ClickableQLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1424, 750)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.videoLabel = ClickableQLabel(self.centralwidget)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setAutoFillBackground(True)

        self.verticalLayout.addWidget(self.videoLabel)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.conversionTab = QWidget()
        self.conversionTab.setObjectName(u"conversionTab")
        self.verticalLayoutConversion = QVBoxLayout(self.conversionTab)
        self.verticalLayoutConversion.setObjectName(u"verticalLayoutConversion")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.loadFileButton = QPushButton(self.conversionTab)
        self.loadFileButton.setObjectName(u"loadFileButton")

        self.verticalLayout_2.addWidget(self.loadFileButton)

        self.pushButton = QPushButton(self.conversionTab)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.conversionTab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.conversionTab)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.outdir_2 = QPushButton(self.conversionTab)
        self.outdir_2.setObjectName(u"outdir_2")

        self.horizontalLayout_3.addWidget(self.outdir_2)

        self.label_7 = QLabel(self.conversionTab)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_3.addWidget(self.label_7)

        self.fpsBox_2 = QComboBox(self.conversionTab)
        self.fpsBox_2.setObjectName(u"fpsBox_2")
        self.fpsBox_2.setEditable(False)

        self.horizontalLayout_3.addWidget(self.fpsBox_2)

        self.label_8 = QLabel(self.conversionTab)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.outputFormatBox = QComboBox(self.conversionTab)
        self.outputFormatBox.setObjectName(u"outputFormatBox")

        self.horizontalLayout_3.addWidget(self.outputFormatBox)

        self.label_5 = QLabel(self.conversionTab)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.fileName_2 = QLineEdit(self.conversionTab)
        self.fileName_2.setObjectName(u"fileName_2")

        self.horizontalLayout_3.addWidget(self.fileName_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.convertButton = QPushButton(self.conversionTab)
        self.convertButton.setObjectName(u"convertButton")

        self.verticalLayout_2.addWidget(self.convertButton)


        self.verticalLayoutConversion.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.conversionTab, "")
        self.cropTab = QWidget()
        self.cropTab.setObjectName(u"cropTab")
        self.cropTabLayout = QVBoxLayout(self.cropTab)
        self.cropTabLayout.setObjectName(u"cropTabLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox1 = QGroupBox(self.cropTab)
        self.groupBox1.setObjectName(u"groupBox1")
        self.horizontalLayout_1 = QHBoxLayout(self.groupBox1)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.loadVideo = QPushButton(self.groupBox1)
        self.loadVideo.setObjectName(u"loadVideo")

        self.horizontalLayout_1.addWidget(self.loadVideo)

        self.pauseButton = QPushButton(self.groupBox1)
        self.pauseButton.setObjectName(u"pauseButton")

        self.horizontalLayout_1.addWidget(self.pauseButton)

        self.resumeButton = QPushButton(self.groupBox1)
        self.resumeButton.setObjectName(u"resumeButton")

        self.horizontalLayout_1.addWidget(self.resumeButton)


        self.horizontalLayout.addWidget(self.groupBox1)

        self.groupBox2 = QGroupBox(self.cropTab)
        self.groupBox2.setObjectName(u"groupBox2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.groupBox2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.outdir = QPushButton(self.groupBox2)
        self.outdir.setObjectName(u"outdir")

        self.horizontalLayout_2.addWidget(self.outdir)

        self.label = QLabel(self.groupBox2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.fpsBox = QComboBox(self.groupBox2)
        self.fpsBox.setObjectName(u"fpsBox")
        self.fpsBox.setEditable(False)

        self.horizontalLayout_2.addWidget(self.fpsBox)

        self.label_2 = QLabel(self.groupBox2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.codecBox = QComboBox(self.groupBox2)
        self.codecBox.setObjectName(u"codecBox")
        self.codecBox.setEditable(False)

        self.horizontalLayout_2.addWidget(self.codecBox)

        self.label_3 = QLabel(self.groupBox2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.fileName = QLineEdit(self.groupBox2)
        self.fileName.setObjectName(u"fileName")

        self.horizontalLayout_2.addWidget(self.fileName)

        self.saveButton = QPushButton(self.groupBox2)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_2.addWidget(self.saveButton)


        self.horizontalLayout.addWidget(self.groupBox2)


        self.cropTabLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.cropTab, "")
        self.trimTab = QWidget()
        self.trimTab.setObjectName(u"trimTab")
        self.trimTabLayout = QVBoxLayout(self.trimTab)
        self.trimTabLayout.setObjectName(u"trimTabLayout")
        self.tabWidget.addTab(self.trimTab, "")
        self.Audio = QWidget()
        self.Audio.setObjectName(u"Audio")
        self.convertTabLayout = QVBoxLayout(self.Audio)
        self.convertTabLayout.setObjectName(u"convertTabLayout")
        self.tabWidget.addTab(self.Audio, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.videoLabel.setText("")
        self.conversionTab.setProperty("title", QCoreApplication.translate("MainWindow", u"Conversion", None))
        self.loadFileButton.setText(QCoreApplication.translate("MainWindow", u"Load File", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"output dir", None))
        self.outdir_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"fps", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"codec", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"output name", None))
        self.fileName_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter output file name...", None))
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"Convert", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.conversionTab), QCoreApplication.translate("MainWindow", u"Convert", None))
        self.groupBox1.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.loadVideo.setText(QCoreApplication.translate("MainWindow", u"Load Video", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.resumeButton.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.groupBox2.setTitle(QCoreApplication.translate("MainWindow", u"Croped Video Settings", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Output dir", None))
        self.outdir.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"fps", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"codec", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"output name", None))
        self.fileName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter output file name...", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save Crop", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cropTab), QCoreApplication.translate("MainWindow", u"Crop", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trimTab), QCoreApplication.translate("MainWindow", u"Trim", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Audio), QCoreApplication.translate("MainWindow", u"Audio", None))
    # retranslateUi

