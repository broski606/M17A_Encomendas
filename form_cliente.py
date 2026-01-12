from PyQt5 import QtWidgets
from Interfaces.formCliente import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formCliente(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_principal):
        super().__init__()
        self.setupUi(self)

        self.form_principal = form_principal
        
        self.pushButton_voltar.clicked.connect(self.voltar)

    def voltar(self):
        self.close()
        self.form_principal.show()

    def listagemclientes(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT * FROM cliente WHERE nome LIKE '%{filtro}%' ORDER BY nome ASC;"
                else:
                    cmd_sql = "SELECT * FROM cliente ORDER BY nome ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "nome", "morada", "telefone","email", "nif"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)
                
                self.tableView.resizeColumnsToContents()
                # Selecionar apenas linhas inteiras
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")