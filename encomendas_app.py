import mysql.connector
from PyQt5 import QtWidgets
import sys
from form_principal import formPrincipal

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        janela = formPrincipal()
        janela.show()
        sys.exit(app.exec_())