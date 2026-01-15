from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formDetalhesArtigo import Ui_Form
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class FormDetalhesArtigo(QtWidgets.QMainWindow,Ui_Form):
    def __init__(self, form_artigos):
        super().__init__()
        self.setupUi(self)
        self.modo_funcionamento = None
        self.designacao = None
        self.preco = None
        self.stock = None
        self.categoria = None
        self.form_artigos = form_artigos

        self.pushButton_voltar.clicked.connect(self.voltar)
        self.pushButton_gravar.clicked.connect(self.gravar)

    def gravar(self):
        #alterado a partir do form_altear_categoria.py e do form_nova_categoria.py
        if self.modo_funcionamento == "novo":
            try:
                id = self.lineEdit_id.text()
                designacao = self.lineEdit_designacao.text()
                preco = self.lineEdit_preco.text()
                stock = self.lineEdit_stock.text()
                categoria = self.comboBox_categoria.currentText()

                if len(id)==0 or len(designacao)==0 or len(preco)==0 or len(stock)==0 or len(categoria)==0:
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
                cmd_sql = f"SELECT COUNT(*) FROM artigo WHERE id = %s OR designacao = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id, designacao,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência da categoria")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe uma categoria com designação {designacao} ou com id {id} introduzidos")
                    return
                
                cmd_sql = "SELECT id FROM categoria WHERE designacao = %s;"
                idCategoria = consultaUmValor(conn_BD, cmd_sql, (categoria,))
                if idCategoria == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o ID da categoria")
                    return
                
                cmd_sql = "INSERT INTO artigo (id, idCategoria, designacao, preco, stock) VALUES (%s, %s, %s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id, idCategoria, designacao, preco, stock))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao inserir o registo")
                    return
                resposta = QtWidgets.QMessageBox.question(self, "Confirmação", "Categoria inserida com sucesso!\n Pretende inserir dados de uma nova categoria?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if resposta == QtWidgets.QMessageBox.Yes:
                    self.inicializar(selecao=None, modo_funcionamento="novo")
                    return
                else:
                    self.voltar()
                conn_BD.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
        
        elif self.modo_funcionamento == "alterar":
            try:
                id = self.lineEdit_id.text()
                designacao = self.lineEdit_designacao.text()
                preco = self.lineEdit_preco.text()
                stock = self.lineEdit_stock.text()
                categoria = self.comboBox_categoria.currentText()

                if len(designacao)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Designacao do artigo por preencher")
                    return

                if self.designacao == designacao:
                    QtWidgets.QMessageBox.critical(self,"Aviso","A designação do artigo não foi alterada")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                cmd_sql = f"SELECT COUNT(*) FROM artigo WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id,))
                cmd_sql = f"SELECT COUNT(*) FROM artigo WHERE designacao = %s;"
                numRegistosD = consultaUmValor(conn_BD, cmd_sql, (designacao,))
                if numRegistosId == -1 or numRegistosD == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do artigo")
                    return
                elif numRegistosD > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe um artigo com designação {designacao} ou com id {id} introduzidos")
                    return
                elif numRegistosId==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar o artigo com identificador {id}!")
                    return
                idCategoria = consultaUmValor(conn_BD, "SELECT id FROM categoria WHERE designacao = %s;", (categoria,))
                cmd_sql = "UPDATE artigo SET designacao = %s, preco = %s, stock = %s, idCategoria = %s WHERE id = %s;"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (designacao, preco, stock, idCategoria, id))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao alterar o registo")
                    return
                QtWidgets.QMessageBox.information(self, "Confirmação", "Artigo alterado com sucesso!")
                
                self.close()
                self.form_artigos.show()
                self.form_artigos.listagemartigos()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
            

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_designacao.setText("")
            self.lineEdit_preco.setText("")
            self.lineEdit_stock.setText("")

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                
                cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_categoria.clear() # Limpa a QComboBox antes de preencher
                    categorias = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_categoria.addItems(categorias) # Adiciona os itens ao QComboBox

                cmd_sql = "SELECT MAX(id)+1 FROM artigo;"
                proximo_id = consultaUmValor(conn_BD, cmd_sql)
                if proximo_id == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o próximo id")
                    return
                self.lineEdit_id.setText(str(proximo_id))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

        elif modo_funcionamento == "alterar":
            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                #preencher COMBOBOX com valores da BD
                cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_categoria.clear() # Limpa a QComboBox antes de preencher
                    categorias = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_categoria.addItems(categorias) # Adiciona os itens ao QComboBox
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

            linha = selecao[0].row() # Primeira linha selecionada
            modelo = self.form_artigos.tableView.model()
            self.lineEdit_id.setText(modelo.data(modelo.index(linha, 0)))
            self.lineEdit_designacao.setText(modelo.data(modelo.index(linha, 2)))
            self.designacao = modelo.data(modelo.index(linha, 2))
            self.lineEdit_preco.setText(modelo.data(modelo.index(linha, 3)))
            self.preco = modelo.data(modelo.index(linha, 3))
            self.lineEdit_stock.setText(modelo.data(modelo.index(linha, 4)))
            self.stock = modelo.data(modelo.index(linha, 4))
            self.comboBox_categoria.setCurrentText(modelo.data(modelo.index(linha, 1)))
            self.categoria = modelo.data(modelo.index(linha, 1))
            self.lineEdit_id.setEnabled(False)



    def voltar(self):
        self.close()
        self.form_artigos.show()
        self.form_artigos.listagemartigos()