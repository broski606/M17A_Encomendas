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

        self.pushButton_apagar.clicked.connect(self.EliminarEncomenda)

    def voltar(self):
        self.close()
        self.form_principal.show()
    
    def EliminarEncomenda(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            nEncomenda = modelo.data(modelo.index(linha, 0))
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                resposta = QtWidgets.QMessageBox.question(self, "Questão", f"Tem certeza de que deseja excluir a encomenda com número {nEncomenda} ?")
                if resposta == QtWidgets.QMessageBox.Yes:
                    # Eliminar o registo da BD
                    cmd_sql = "DELETE detalheencomenda, encomenda FROM encomenda LEFT JOIN detalheencomenda ON encomenda.nEncomenda = detalheencomenda.nEncomenda WHERE encomenda.nEncomenda = %s;"
                    num_registos= operacao_DML(conn_BD,cmd_sql,(nEncomenda,))
                    if num_registos > 0: 
                        QtWidgets.QMessageBox.information(self, "Sucesso", "A eliminação do registo foi bem sucedida!")
                        self.listagemencomendas()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi eliminado !")
                else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "A eliminação do registo foi cancelada!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o registo da encomenda a eliminar!")


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
                    linha = selecao[0].row() # primeira linha selecionada
                    modelo = self.tableView.model()
                    nEncomenda = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
                    cmd_sql = f"SELECT idArtigo, designacao, quantidade FROM detalheencomenda, artigo WHERE artigo.id = detalheencomenda.idArtigo AND nEncomenda = {nEncomenda} ORDER BY idArtigo ASC;"
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
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
                elif len(filtro) == 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"

                elif len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                    cmd_sql = f"SELECT encomenda.nEncomenda, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
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