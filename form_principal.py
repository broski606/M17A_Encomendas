from PyQt5 import QtWidgets
from Interfaces.formPrincipal import Ui_MainWindow
from form_categorias import formCategorias
from form_artigos import formArtigos
from form_cliente import formCliente
from form_encomendas import formEncomendas

class formPrincipal(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.form_categorias = formCategorias(self)
        self.form_artigos = formArtigos(self)
        self.form_cliente = formCliente(self)
        self.form_encomendas = formEncomendas(self)

        self.pushButton_sair.clicked.connect(self.sair)
        self.pushButton_categorias.clicked.connect(self.mostrar_form_categorias)
        self.pushButton_clientes.clicked.connect(self.mostrar_form_clientes)
        self.pushButton_produtos.clicked.connect(self.mostrar_form_artigos)
        self.pushButton_encomendas.clicked.connect(self.mostrar_form_encomendas)
        
    def sair(self):
        self.close()

    def mostrar_form_categorias(self):
        self.hide()
        self.form_categorias.show()
        self.form_categorias.listagemCategorias()

    def mostrar_form_clientes(self):
        self.hide()
        self.form_cliente.show()
        self.form_cliente.listagemclientes()

    def mostrar_form_artigos(self):
        self.hide()
        self.form_artigos.show()
        self.form_artigos.listagemartigos()
    
    def mostrar_form_encomendas(self):
        self.hide()
        self.form_encomendas.show()
        self.form_encomendas.listagemencomendas()