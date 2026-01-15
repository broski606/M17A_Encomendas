from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formCategorias import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from form_nova_categoria import formNovaCategoria
from form_alterar_categoria import formAlterarCategoria

class formCategorias(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_principal):
        super().__init__()
        self.setupUi(self)

        self.form_principal = form_principal

        self.form_nova_categoria = formNovaCategoria(self)

        self.form_alterar_categoria = formAlterarCategoria(self)

        self.pushButton_voltar.clicked.connect(self.voltar)

        self.pushButton_eliminar.clicked.connect(self.EliminarCategoria)
        
        self.pushButton_novo.clicked.connect(self.novo)

        self.pushButton_editar.clicked.connect(self.alterar)

        self.pushButton_limpar.clicked.connect(self.LimparFiltro)

        self.lineEdit.returnPressed.connect(self.listagemCategorias)
        self.pushButton_filtrar.clicked.connect(self.listagemCategorias)


    def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return
        
        self.hide()
        self.form_alterar_categoria.show()
        self.form_alterar_categoria.inicializar(selecao)

    def novo(self):
        self.hide()
        self.form_nova_categoria.show()
        self.form_nova_categoria.inicializar()


    def voltar(self):
        self.close()
        self.form_principal.show()

    def listagemCategorias(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT * FROM Categoria WHERE designacao LIKE '%{filtro}%' ORDER BY designacao ASC;"
                else:
                    cmd_sql = "SELECT * FROM Categoria ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)

                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["Identificador", "Designação"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                self.tableView.resizeColumnsToContents()

                # Selecionar apenas linhas inteiras
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                # Selecionar apenas uma linha de cada vez
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                #Verificar propriedades de uma QTableView para que as células não sejam editáveis:
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def LimparFiltro(self):
        self.lineEdit.setText("") 
        #self.lineEdit.clear()
        self.listagemCategorias()

    def EliminarCategoria(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            id_categoria = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
            nome_categoria = modelo.data(modelo.index(linha,1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                cmd_sql = "SELECT COUNT(*) FROM artigo WHERE idCategoria = %s;"
                num_registos = consultaUmValor(conn_BD,cmd_sql,(id_categoria,))
                if num_registos == 0:
                    resposta = QtWidgets.QMessageBox.question(self, "Questão", f"Tem certeza de que deseja excluir a categoria com identificador {id_categoria} e designação {nome_categoria}?")
                    if resposta == QtWidgets.QMessageBox.Yes:
                            # Eliminar o registo da BD
                            cmd_sql = "DELETE FROM Categoria WHERE id = %s;"
                            num_registos= operacao_DML(conn_BD,cmd_sql,(id_categoria,))
                            if num_registos > 0: 
                                QtWidgets.QMessageBox.information(self, "Sucesso", "A eliminação do registo foi bem sucedida!")
                                self.listagemCategorias()
                            else:
                                QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi eliminado !")
                    else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "A eliminação do registo foi cancelada!")
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso",f"Não é possível eliminar a categoria {nome_categoria} pois existem artigos associados a essa categoria!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o registo da categoria a eliminar!")
