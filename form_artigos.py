from PyQt5 import QtWidgets
from Interfaces.formArtigos import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class formArtigos(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_principal):
        super().__init__()
        self.setupUi(self)

        self.form_principal = form_principal
        self.pushButton_voltar.clicked.connect(self.voltar)
        self.pushButton_6.clicked.connect(self.EliminarArtigo)
        self.pushButton_2.clicked.connect(self.listagemartigos)


    def listagemartigos(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT * FROM artigo WHERE designacao LIKE '%{filtro}%' ORDER BY designacao ASC;"
                else:
                    cmd_sql = "SELECT * FROM artigo ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "id de categoria", "designação", "preco", "stock"])
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
    
    def LimparFiltro(self):
        self.lineEdit.setText("") 
        #self.lineEdit.clear()
        self.listagemartigos()
    
    def EliminarArtigo(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            id_artigo = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
            nome_artigo = modelo.data(modelo.index(linha,1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                cmd_sql = "SELECT COUNT(*) FROM detalheencomenda WHERE idArtigo = %s;"
                num_registos = consultaUmValor(conn_BD,cmd_sql,(id_artigo,))
                if num_registos == 0:
                    resposta = QtWidgets.QMessageBox.question(self, "Questão", f"Tem certeza de que deseja excluir o artigo com identificador {id_artigo} e designação {nome_artigo}?")
                    if resposta == QtWidgets.QMessageBox.Yes:
                            # Eliminar o registo da BD
                            cmd_sql = "DELETE FROM artigo WHERE id = %s;"
                            num_registos= operacao_DML(conn_BD,cmd_sql,(id_artigo,))
                            if num_registos > 0: 
                                QtWidgets.QMessageBox.information(self, "Sucesso", "A eliminação do registo foi bem sucedida!")
                                self.listagemCategorias()
                            else:
                                QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi eliminado !")
                    else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "A eliminação do registo foi cancelada!")
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso",f"Não é possível eliminar o artigo {nome_artigo} pois existem encomendas associados a esse artigo!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o registo do artigo a eliminar!")
    
    def voltar(self):
        self.close()
        self.form_principal.show()