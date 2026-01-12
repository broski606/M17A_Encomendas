from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formNovaCategoria import Ui_Form
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class formNovaCategoria(QtWidgets.QMainWindow,Ui_Form):
    def __init__(self, form_categorias):
        super().__init__()
        self.setupUi(self)

        self.form_categorias = form_categorias

        self.pushButton_voltar.clicked.connect(self.voltar)
        self.pushButton_gravar.clicked.connect(self.gravar)
        self.inicializar()

    def gravar(self):
        try:
            id = self.lineEdit_id.text()
            designacao = self.lineEdit_designacao.text()
            if len(id)==0 or len(designacao)==0:
                QtWidgets.QMessageBox.critical(self,"Aviso","Campos por preencher")
                return
            tipoDados_id = verificar_tipo_dados(id)
            if tipoDados_id != "inteiro":
                QtWidgets.QMessageBox.critical(self,"Aviso","Inserir valor inteiro no campo id")
                return
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                return
            cmd_sql = f"SELECT COUNT(*) FROM categoria WHERE id = %s OR designacao = %s;"
            numRegistos = consultaUmValor(conn_BD, cmd_sql, (id, designacao,))
            if numRegistos == -1:
                QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência da categoria")
                return
            elif numRegistos > 0:
                QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe uma categoria com designação {designacao} ou com id {id} introduzidos")
                return
            cmd_sql = "INSERT INTO categoria (id, designacao) VALUES (%s, %s);"
            numRegistos = operacao_DML(conn_BD, cmd_sql, (id, designacao))
            if numRegistos == -1:
                QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao inserir o registo")
                return
            resposta = QtWidgets.QMessageBox.question(self, "Confirmação", "Categoria inserida com sucesso!\n Pretende inserir dados de uma nova categoria?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if resposta == QtWidgets.QMessageBox.Yes:
                self.inicializar()
                return
            else:
                self.voltar()
            conn_BD.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
            return

    def inicializar(self):
        self.lineEdit_designacao.setText("")
        try:
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                return
            cmd_sql = "SELECT MAX(id)+1 FROM categoria;"
            proximo_id = consultaUmValor(conn_BD, cmd_sql)
            if proximo_id == -1:
                QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o próximo id")
                return
            self.lineEdit_id.setText(str(proximo_id))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def voltar(self):
        self.close()
        self.form_categorias.show()
        self.form_categorias.listagemCategorias()