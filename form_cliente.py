from PyQt5 import QtWidgets
from Interfaces.formCliente import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from form_detalhes_cliente import FormDetalhesCliente

class formCliente(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_principal):
        super().__init__()
        self.setupUi(self)

        self.form_principal = form_principal
        self.form_detalhes_cliente = FormDetalhesCliente(self)
        
        self.pushButton_voltar.clicked.connect(self.voltar)
        self.pushButton_6.clicked.connect(self.EliminarCliente)
        self.pushButton_3.clicked.connect(self.LimparFiltro)
        self.pushButton_2.clicked.connect(self.listagemclientes)
        self.pushButton_7.clicked.connect(self.novo)
        self.pushButton_4.clicked.connect(self.alterar)

    def voltar(self):
        self.close()
        self.form_principal.show()

    def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return
        
        self.hide()
        self.form_detalhes_cliente.show()
        self.form_detalhes_cliente.inicializar(selecao, "alterar")

    def novo(self):
        self.hide()
        self.form_detalhes_cliente.show()
        self.form_detalhes_cliente.inicializar(None, "novo")

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
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")
        
    def LimparFiltro(self):
        self.lineEdit.setText("")
        self.listagemclientes()

    def EliminarCliente(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row()
            modelo = self.tableView.model()
            id_cliente = modelo.data(modelo.index(linha, 0))
            nome_cliente = modelo.data(modelo.index(linha,1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                cmd_sql = "SELECT COUNT(*) FROM encomenda WHERE idCliente = %s;"
                num_registos = consultaUmValor(conn_BD,cmd_sql,(id_cliente,))
                if num_registos == 0:
                    resposta = QtWidgets.QMessageBox.question(self, "Questão", f"Tem certeza de que deseja excluir o cliente com identificador {id_cliente} e nome {nome_cliente}?")
                    if resposta == QtWidgets.QMessageBox.Yes:
                            cmd_sql = "DELETE FROM cliente WHERE id = %s;"
                            num_registos= operacao_DML(conn_BD,cmd_sql,(id_cliente,))
                            if num_registos > 0: 
                                QtWidgets.QMessageBox.information(self, "Sucesso", "A eliminação do registo foi bem sucedida!")
                                self.listagemclientes()
                            else:
                                QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi eliminado !")
                    else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "A eliminação do registo foi cancelada!")
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso",f"Não é possível eliminar o cliente {nome_cliente} pois existem encomendas associadas a esse cliente!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o registo do cliente a eliminar!")