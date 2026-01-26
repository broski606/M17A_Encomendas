from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formEncomendas import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formEncomendas(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_principal):
        super().__init__()
        self.setupUi(self)

        self.form_principal = form_principal
        
        self.pushButton_voltar.clicked.connect(self.voltar)
        
        self.pushButton_2.clicked.connect(self.listagemencomendas)

        self.pushButton_limpar.clicked.connect(self.LimparFiltro)

    def voltar(self):
        self.close()
        self.form_principal.show()

    def LimparFiltro(self):
        self.lineEdit.setText("")

        self.radioButton.setAutoExclusive(False)
        self.radioButton_2.setAutoExclusive(False)

        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        
        self.radioButton.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(True)

        self.listagemencomendas()
    
    def listagemdetalhesencomenda(self, selecao):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                selecao = self.tableView.selectionModel().selectedRows()
                if selecao:
                    cmd_sql = f"SELECT idArtigo, designacao, quantidade FROM detalheencomenda, artigo WHERE artigo.id = detalheencomenda.idArtigo AND nEncomenda = {selecao[0].row()} ORDER BY idArtigo ASC;"
                    
                    dados = listagem_BD(conn_BD, cmd_sql)
                    modelo = QStandardItemModel()
                    modelo.setHorizontalHeaderLabels(["Id. Artigo","Designação", "Quantidade"])
                    for linha in dados:
                        modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                    self.tableView_2.setModel(modelo)
                    self.tableView_2.resizeColumnsToContents()
                else:
                    return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def listagemencomendas(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False: #Cábula: radioButton1 - Entregues e radioButton2 - Por entregar
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
                elif len(filtro) == 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, detalheencomenda, cliente WHERE encomenda.nEncomenda = detalheencomenda.nEncomenda AND encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["N.ºEncomenda", "Cliente", "Data Encomenda", "Data Entrega"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                #Chamar a atualização dos detalhes da encomenda
                self.tableView.selectionModel().selectionChanged.connect(self.listagemdetalhesencomenda)
                
                self.tableView.resizeColumnsToContents()
                # Selecionar apenas linhas inteiras
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")