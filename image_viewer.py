import sys
import os

from PySide2 import QtWidgets
from PySide2.QtWidgets import QSizePolicy ,QFileSystemModel, QStyle
from PySide2.QtCore import Qt, QDir, QFile, QFileInfo, QSize
from PySide2.QtGui import QImage, QPixmap, QPalette, QColor, QKeySequence


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Gallery (from Epic Codes from Angry Coders)")
		self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
		size = QSize(537, 450)
		self.setGeometry(QStyle.alignedRect(
							Qt.LeftToRight, 
							Qt.AlignCenter, 
							size, 
							QtWidgets.QApplication.desktop().availableGeometry())
						)
		style = self.setStyle()
		

		layout = QtWidgets.QVBoxLayout()

		self.columnView = QtWidgets.QColumnView()
		self.columnView.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)

		self.displayer = QtWidgets.QLabel()
		self.displayer.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		self.columnView.setPreviewWidget(self.displayer)

		layout.addWidget(self.columnView)

		self.model = QFileSystemModel()
		self.model.setRootPath(QDir.rootPath()) # model's rootPath will be C:

		# bellow 2 lines: let just show image formats in the systemfile
		self.model.setNameFilters(["*.png", "*.jpg"])
		self.model.setNameFilterDisables(False)

		path = QDir.currentPath()	# gets the current program's directory
		self.columnView.setModel(self.model)
		
		# below: sets the Sub-Path for the Widget
		## change this too root to be able to see whole system directories
		self.columnView.setRootIndex(self.model.index(QDir.currentPath()))

		hor_layout = QtWidgets.QHBoxLayout()

		self.open_button = QtWidgets.QPushButton("open")
		self.open_button.clicked.connect(self.fileOpened)
		self.open_button.setFixedSize(200,50)
		self.open_button.setShortcut(QKeySequence(Qt.Key_Return))
		hor_layout.addWidget(self.open_button)


		self.close_button = QtWidgets.QPushButton("exit")
		self.close_button.pressed.connect(self.closeApp)
		self.close_button.setFixedSize(200,50)
		hor_layout.addWidget(self.close_button)

		layout.addLayout(hor_layout)

		container = QtWidgets.QWidget()
		container.setLayout(layout)


		self.setCentralWidget(container)



	def fileOpened(self):
		selectionModel = self.columnView.selectionModel()
		indexes = selectionModel.selectedIndexes()
		if indexes:
			index = indexes[0]
			file_path = self.model.filePath(index)
			file = QFile(file_path)
			file_name = QFileInfo(file).fileName()  # if no extention -> baseName
			file_name_format = QFileInfo(file).suffix()
			file_formats = ["png", "jpg", "jpeg"]
			if file_name_format in file_formats:
				image = QPixmap(file_name)
				width = self.columnView.columnWidths()[0]
				self.displayer.setPixmap(QPixmap(image.scaled(width, width, Qt.KeepAspectRatio)))

	def closeApp(self):
		self.close()

	def setStyle(self):
		style_text = "QWidget{background-color: rgb(42,42,42); color: rgb(180,180,180); selection-background-color: rgb(80,80,80); selection-color:white}"
		style_text += ".QWidget{background-color:rgb(53,53,53)}"
		style_text += "QPushButton{background-color: rgb(72,72,72)}"
		self.setStyleSheet(style_text)

	
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setStyle("Fusion")
	w = MainWindow()
	w.show()
	app.exec_()


