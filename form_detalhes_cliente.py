from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formDetalhesCliente import Ui_Form
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class FormDetalhesCliente(QtWidgets.QMainWindow,Ui_Form):
    def __init__(self, form_cliente):
        super().__init__()
        self.setupUi(self)
        self.modo_funcionamento = None
        self.nome = None
        self.morada = None
        self.telefone = None
        self.email = None
        self.nif = None
        self.form_cliente = form_cliente

        self.pushButton_voltar.clicked.connect(self.voltar)
        self.pushButton_gravar.clicked.connect(self.gravar)

    def gravar(self):
        if self.modo_funcionamento == "novo":
            try:
                id = self.lineEdit_id.text()
                nome = self.lineEdit_nome.text()
                morada = self.plainTextEdit_morada.toPlainText()
                telefone = self.lineEdit_telefone.text()
                email = self.lineEdit_email.text()
                nif = self.lineEdit_nif.text()

                if len(id)==0 or len(nome)==0 or len(morada)==0 or len(telefone)==0 or len(email)==0 or len(nif)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Campos por preencher")
                    return
                tipoDados_id = verificar_tipo_dados(id)
                if tipoDados_id != "inteiro":
                    QtWidgets.QMessageBox.critical(self,"Aviso","Inserir valor inteiro no campo id")
                    return
                
                tipoDados_nif = verificar_tipo_dados(nif)
                if tipoDados_nif != "inteiro":
                    QtWidgets.QMessageBox.critical(self,"Aviso","Inserir valor inteiro no campo nif")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                cmd_sql = f"SELECT COUNT(*) FROM cliente WHERE id = %s OR nif = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id, nif,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do cliente")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe um cliente com nif {nif} ou com id {id} introduzidos")
                    return
                
                cmd_sql = "INSERT INTO cliente (id, nome, morada, telefone, email, nif) VALUES (%s, %s, %s, %s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id, nome, morada, telefone, email, nif))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao inserir o registo")
                    return
                resposta = QtWidgets.QMessageBox.question(self, "Confirmação", "Cliente inserido com sucesso!\n Pretende inserir dados de um novo cliente?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
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
                nome = self.lineEdit_nome.text()
                morada = self.plainTextEdit_morada.toPlainText()
                telefone = self.lineEdit_telefone.text()
                email = self.lineEdit_email.text()
                nif = self.lineEdit_nif.text()

                if len(nome)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Nome do cliente por preencher")
                    return

                if self.nome == nome and self.nif == nif:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Os dados do cliente não foram alterados")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                cmd_sql = f"SELECT COUNT(*) FROM cliente WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id,))
                if numRegistosId == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do cliente")
                    return
                elif numRegistosId==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar o cliente com identificador {id}!")
                    return
                
                cmd_sql = "UPDATE cliente SET nome = %s, morada = %s, telefone = %s, email = %s, nif = %s WHERE id = %s;"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (nome, morada, telefone, email, nif, id))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao alterar o registo")
                    return
                QtWidgets.QMessageBox.information(self, "Confirmação", "Cliente alterado com sucesso!")
                
                self.close()
                self.form_cliente.show()
                self.form_cliente.listagemclientes()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
            

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_nome.setText("")
            self.plainTextEdit_morada.setPlainText("")
            self.lineEdit_telefone.setText("")
            self.lineEdit_email.setText("")
            self.lineEdit_nif.setText("")

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return

                cmd_sql = "SELECT MAX(id)+1 FROM cliente;"
                proximo_id = consultaUmValor(conn_BD, cmd_sql)
                if proximo_id == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o próximo id")
                    return
                self.lineEdit_id.setText(str(proximo_id))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

        elif modo_funcionamento == "alterar":
            linha = selecao[0].row() # Primeira linha selecionada
            modelo = self.form_cliente.tableView.model()
            self.lineEdit_id.setText(modelo.data(modelo.index(linha, 0)))
            self.nome = modelo.data(modelo.index(linha, 1))
            self.lineEdit_nome.setText(self.nome)

            self.morada = modelo.data(modelo.index(linha, 2))
            self.plainTextEdit_morada.setPlainText(self.morada)

            self.telefone = modelo.data(modelo.index(linha, 3))
            self.lineEdit_telefone.setText(self.telefone)

            self.email = modelo.data(modelo.index(linha, 4))
            self.lineEdit_email.setText(self.email)
            
            self.nif = modelo.data(modelo.index(linha, 5))
            self.lineEdit_nif.setText(self.nif)

            self.lineEdit_id.setEnabled(False)



    def voltar(self):
        self.close()
        self.form_cliente.show()
        self.form_cliente.listagemclientes()