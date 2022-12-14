#Caption:
#cb: combobox
#gb: groupbox
#lb: label
#le: lineedit
#pb: pushbutton
#rb: radiobutton

from classes.main import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

class form(QMainWindow):   # Fill in the necessary data of a "CT-e"
    def __init__(self, usuario, senha):
        super(form, self).__init__()
        uic.loadUi("ui\\main_window.ui", self)
        self.usuario = usuario
        self.senha = senha
        self.inserir_primeiro_cte = False
        self.config()
        self.show()
        self.cbFormadePagamento.currentTextChanged.connect(self.forma_pagamento_changed)
        self.rbSim.toggled.connect(self.rbSim_toggled)
        self.rbNao.toggled.connect(self.rbNao_toggled)
        self.pbProcurarFatura.clicked.connect(self.encontrar_fatura)
        self.pbLocalizacaoCte.clicked.connect(self.encontrar_pasta_cte)
        self.pbLimpar.clicked.connect(self.limpar)
        self.pbIniciar.clicked.connect(self.iniciar)

    # Initialize the elements of the window.
    def config(self):
        self.rbInvisible.setVisible(False) # Invisible button to force others to be unchecked in specific situations.
        self.rbInvisible_2.setVisible(False) # Invisible button to force others to be unchecked in specific situations.
        self.leFatura.setReadOnly(True)
        self.leLocalizacaoCte.setReadOnly(True)

    # When "Forma de pagamento" combobox is changed:
    def forma_pagamento_changed(self):
        if self.cbFormadePagamento.currentText() == "Boleto Agrupado":
            self.gbPrimeiraNota.setEnabled(True) 
            self.lbPrimeiraNota.setEnabled(True)
            self.rbSim.setEnabled(True) 
            self.rbNao.setEnabled(True)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.leFatura.setText("")

        elif self.cbFormadePagamento.currentText() == "Boleto em Anexo":
            self.rbInvisible.setChecked(True)
            self.gbPrimeiraNota.setEnabled(False) 
            self.lbPrimeiraNota.setEnabled(False)
            self.rbSim.setEnabled(False) 
            self.rbNao.setEnabled(False)
            self.pbProcurarFatura.setEnabled(True)
            self.leFatura.setEnabled(True)

        else:
            self.rbInvisible.setChecked(True)
            self.gbPrimeiraNota.setEnabled(False) 
            self.lbPrimeiraNota.setEnabled(False)
            self.rbSim.setEnabled(False) 
            self.rbNao.setEnabled(False)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.leFatura.setText("")

    # When "Yes" button is toggled:
    def rbSim_toggled(self):
        if self.rbSim.isChecked() == True:
            self.lbPrimeiroCte.setEnabled(True)
            self.lePrimeiroCte.setEnabled(True)
            self.inserir_primeiro_cte = False
        else:
            self.lePrimeiroCte.setEnabled(False)
            self.lePrimeiroCte.setEnabled(False)
            self.inserir_primeiro_cte = True
            self.lePrimeiroCte.setText("")

    # When "No" button is toggled:
    def rbNao_toggled(self):
        if self.rbNao.isChecked() == True:
            self.gbFatura.setEnabled(True)
            self.leFatura.setEnabled(True)
            self.pbProcurarFatura.setEnabled(True)
        else:
            self.gbFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setText("")    

    # Button to search for "fatura".
    def encontrar_fatura(self): 
        path = QFileDialog.getOpenFileName()
        path = self.leFatura.setText(path[0])        

    # Button to serch for the path of the "CT-e" documents.
    def encontrar_pasta_cte(self):
        path = QFileDialog.getExistingDirectory()
        path = self.leLocalizacaoCte.setText(path)

    # Store data in variables.
    def salvar_dados(self):
        if self.rbCitroen.isChecked():
            self.unidade = "11.458.618/0001-16"
        elif self.rbJeep.isChecked():
            self.unidade = "21.214.513/0001-75"
        elif self.rbVolkswagen.isChecked():
            self.unidade = "03.267.961/0001-55"
        elif self.rbParque.isChecked():
            self.unidade = "03.267.961/0004-06"
        
        self.data_vencimento = self.leDatadeVencimento.text()
        self.forma_pagamento = self.cbFormadePagamento.currentText()

        if self.forma_pagamento == "Boleto Agrupado":
            if self.rbSim.isChecked():
                self.inserir_primeiro_cte = False
            elif self.rbNao.isChecked:
                self.inserir_primeiro_cte = True
        else:
            pass
        
        self.fatura_path = self.leFatura
        self.cte_lista = (self.pteCte.toPlainText()).split()
    
    def limpar(self):
        self.rbInvisible_2.setChecked(True)
        self.rbInvisible.setChecked(True)
        self.cbFormadePagamento.setCurrentText("")
        self.lePrimeiroCte.setText("")
        self.leDatadeVencimento.setText("")
        self.leFatura.setText("")
        self.leLocalizacaoCte.setText("")
        self.pteCte.setPlainText("")

    def iniciar(self):
        # Validation.
        if self.rbCitroen.isChecked() == False and self.rbJeep.isChecked() == False and self.rbVolkswagen.isChecked() == False and self.rbParque.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a unidade.")
        elif self.cbFormadePagamento.currentText() == "":
            QMessageBox.about(self, "Alerta", "Selecione a forma de pagamento.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == False and self.rbNao.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a opção relacionada a inserção da primeira nota.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == True and  self.lePrimeiroCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira o número do primeiro CT-e.")
        elif self.leDatadeVencimento.text() == "//":
            QMessageBox.about(self, "Alerta", "Digite a data de vencimento.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == True and  self.leLocalizacaoCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")                   
        elif self.leFatura.text() == "" and self.rbSim.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Insira a Fatura.")
        elif self.leLocalizacaoCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")
        elif self.pteCte.toPlainText() == "":
            QMessageBox.about(self, "Alerta", "Digite o(s) número(s) do(s) documento(s) de CT-e.")
        # Create an instance of the automation code.
        else:
            self.salvar_dados()
            self.main = main(self.usuario, self.senha, self.unidade, self.cbFormadePagamento.currentText(), self.inserir_primeiro_cte, self.lePrimeiroCte.text(), self.leDatadeVencimento.text(), self.leFatura.text(), self.leLocalizacaoCte.text(), self.cte_lista)
### End of class "main_window".