from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi("mainwindow.ui", self)

		self.modifcarTimer = QTimer(self)
		self.modifcarTimer.setSingleShot(True)
		self.modifcarTimer.setInterval(1000)
		self.modifcarTimer.timeout.connect(self.onModificarTimer_timeout)

		self.buscarModel = QSqlQueryModel(self)
		self.buscarModel.setQuery("select * from empleado")
		self.buscar_tableview.setModel(self.buscarModel)

		self.eliminarModel = QSqlTableModel(self)
		self.eliminarModel.setTable("empleado")
		self.eliminarModel.select()
		self.eliminar_tableview.setEditTriggers(QTableView.NoEditTriggers)
		self.eliminar_tableview.setSelectionBehavior(QTableView.SelectRows)
		self.eliminar_tableview.setModel(self.eliminarModel)

		self.modificarModel = QSqlTableModel(self)
		self.modificarModel.setTable("empleado")
		self.modificarModel.select()
		self.modificar_tableview.setModel(self.modificarModel)

		self.buscar_nombre_lineedit.textEdited.connect(self.onBuscar_nombre_lineedit_textEdited)
		self.agregar_button.clicked.connect(self.onAgregar_button_clicked)
		self.eliminar_tableview.clicked.connect(self.onEliminar_tableview_clicked)
		self.modificarModel.beforeUpdate.connect(self.onModificarModel_beforeUpdate)
		self.actionSalir.triggered.connect(self.close)

	def onModificarModel_beforeUpdate(self, row, record):
		self.modifcarTimer.start()

	def refreshTables(self):
		self.buscarModel.setQuery("select * from empleado")
		self.eliminarModel.select()
		self.modificarModel.select()

	def onModificarTimer_timeout(self):
		self.refreshTables()

	def onEliminar_tableview_clicked(self, idx):
		if QMessageBox.question(self, "Eliminar", "¿Está seguro de eliminar?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			row = idx.row()
			if self.eliminarModel.removeRow(row):
				self.eliminarModel.select()

	def onBuscar_nombre_lineedit_textEdited(self, txt):
		self.buscarModel.setQuery("select * from empleado where nombre like '%" + txt + "%'")

	def onAgregar_button_clicked(self):
		nombre = self.nombre_lineedit.text()
		edad = self.edad_lineedit.text()
		salario = self.salario_lineedit.text()

		if (nombre == ""):
			QMessageBox.critical(self, "Error", "El nombre está vacío")
			return
		if (edad == ""):
			QMessageBox.critical(self, "Error", "La edad está vacía")
			return
		if (salario == ""):
			QMessageBox.critical(self, "Error", "El salario está vacío")
			return

		edad = int(edad)
		salario = float(salario)

		q = QSqlQuery()
		if (q.prepare("insert into empleado (nombre, edad, salario) values (?,?,?)")):
			q.addBindValue(nombre)
			q.addBindValue(edad)
			q.addBindValue(salario)
			if (q.exec()):
				if (QMessageBox.question(self, "OK", "Listo, ¿desea borrar los campos?", QMessageBox.Yes | QMessageBox.No)
					== QMessageBox.Yes):
					self.nombre_lineedit.clear()
					self.edad_lineedit.clear()
					self.salario_lineedit.clear()
