# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\aiLab3\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from lab3.CPT import NetWork


class UiDialog(object):
    def __init__(self):
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.label = QtWidgets.QLabel(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(755, 301)
        self.gridLayout.setObjectName("gridLayout")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(self.initBayesNet)
        self.pushButton_2.clicked.connect(self.queryBayes)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "FileName"))
        self.label_2.setText(_translate("Dialog", "QuerySentence"))
        self.pushButton_2.setText(_translate("Dialog", "Query"))
        self.label_3.setText(_translate("Dialog", "Query Answer"))
        self.pushButton.setText(_translate("Dialog", "initBayes"))

    def initBayesNet(self):
        self.bayesNet = NetWork()
        print(self.lineEdit.text())
        self.bayesNet.initFromFile(self.lineEdit.text())

    def queryBayes(self):
        querySentence = self.lineEdit_2.text()
        result = self.bayesNet.query(querySentence)

        queryResult = '\nThe probability that query variable is TRUE is: \n' + str(
            round(result[0], 5)) + '\n\nThe probability that query variable is FALSE is: \n' + str(
            round(result[1], 5))

        self.plainTextEdit.setPlainText(queryResult)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
