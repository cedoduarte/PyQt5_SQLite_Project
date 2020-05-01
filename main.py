from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import *
from mainwindow import MainWindow
import sys

def prepareDatabase():
	db = QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("data.db")
	if (db.open()):
		q = QSqlQuery()
		if (q.prepare("create table if not exists empleado(id integer primary key autoincrement not null, nombre text not null, edad integer not null, salario double not null)")):
			if (q.exec()):
				print("tabla empleado creada satisfactoriamente")

def start():
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	prepareDatabase()
	start()