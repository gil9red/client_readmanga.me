# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 546)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter_main = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_main.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_main.setObjectName("splitter_main")
        self.splitter = QtWidgets.QSplitter(self.splitter_main)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(self.widget_2)
        self.line_edit_search.setProperty("clearButtonEnabled", True)
        self.line_edit_search.setObjectName("line_edit_search")
        self.verticalLayout.addWidget(self.line_edit_search)
        self.list_widget_search_result = QtWidgets.QListWidget(self.widget_2)
        self.list_widget_search_result.setObjectName("list_widget_search_result")
        self.verticalLayout.addWidget(self.list_widget_search_result)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_manga_name = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_manga_name.setFont(font)
        self.label_manga_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_manga_name.setWordWrap(True)
        self.label_manga_name.setObjectName("label_manga_name")
        self.verticalLayout_2.addWidget(self.label_manga_name)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.text_edit_description = QtWidgets.QTextEdit(self.widget)
        self.text_edit_description.setReadOnly(True)
        self.text_edit_description.setObjectName("text_edit_description")
        self.verticalLayout_2.addWidget(self.text_edit_description)
        self.widget_3 = QtWidgets.QWidget(self.splitter_main)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.combo_box_manga_chapters = QtWidgets.QComboBox(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_manga_chapters.sizePolicy().hasHeightForWidth())
        self.combo_box_manga_chapters.setSizePolicy(sizePolicy)
        self.combo_box_manga_chapters.setMaxVisibleItems(30)
        self.combo_box_manga_chapters.setObjectName("combo_box_manga_chapters")
        self.horizontalLayout.addWidget(self.combo_box_manga_chapters)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.scroll_area_image_page = QtWidgets.QScrollArea(self.widget_3)
        self.scroll_area_image_page.setFrameShape(QtWidgets.QFrame.Panel)
        self.scroll_area_image_page.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area_image_page.setWidgetResizable(True)
        self.scroll_area_image_page.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_image_page.setObjectName("scroll_area_image_page")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 274, 408))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scroll_area_image_page.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scroll_area_image_page)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combo_box_pages = QtWidgets.QComboBox(self.widget_3)
        self.combo_box_pages.setMaximumSize(QtCore.QSize(60, 16777215))
        self.combo_box_pages.setObjectName("combo_box_pages")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.combo_box_pages.addItem("")
        self.horizontalLayout_2.addWidget(self.combo_box_pages)
        self.push_button_prev_page = QtWidgets.QPushButton(self.widget_3)
        self.push_button_prev_page.setObjectName("push_button_prev_page")
        self.horizontalLayout_2.addWidget(self.push_button_prev_page)
        self.push_button_next_page = QtWidgets.QPushButton(self.widget_3)
        self.push_button_next_page.setObjectName("push_button_next_page")
        self.horizontalLayout_2.addWidget(self.push_button_next_page)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.splitter_main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 671, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.line_edit_search.setPlaceholderText(_translate("MainWindow", "Введите название манги..."))
        self.label_manga_name.setText(_translate("MainWindow", "<label_manga_name>"))
        self.label_2.setText(_translate("MainWindow", "Описание:"))
        self.text_edit_description.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Главы:"))
        self.combo_box_pages.setProperty("currentText", _translate("MainWindow", "1"))
        self.combo_box_pages.setItemText(0, _translate("MainWindow", "1"))
        self.combo_box_pages.setItemText(1, _translate("MainWindow", "2"))
        self.combo_box_pages.setItemText(2, _translate("MainWindow", "3"))
        self.combo_box_pages.setItemText(3, _translate("MainWindow", "4"))
        self.combo_box_pages.setItemText(4, _translate("MainWindow", "5"))
        self.combo_box_pages.setItemText(5, _translate("MainWindow", "6"))
        self.combo_box_pages.setItemText(6, _translate("MainWindow", "7"))
        self.combo_box_pages.setItemText(7, _translate("MainWindow", "8"))
        self.combo_box_pages.setItemText(8, _translate("MainWindow", "999"))
        self.push_button_prev_page.setText(_translate("MainWindow", "Предыдущая"))
        self.push_button_next_page.setText(_translate("MainWindow", "Следующая"))

