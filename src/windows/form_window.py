# Contractions:
# cb: combobox
# gb: groupbox
# lb: label
# le: lineedit
# pb: pushbutton
# rb: radiobutton

from src.main import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

class Form(QMainWindow):   # Fill in the necessary data of a "CT-e"
    def __init__(self, user, password):
        super(Form, self).__init__()
        uic.loadUi("ui\\form_window.ui", self)
        self.user = user
        self.password = password
        self.insert_first_cte = False
        self.config()
        self.show()
        self.cbPaymentMethod.currentTextChanged.connect(self.payment_method_changed)
        self.rbYes.toggled.connect(self.rbYes_toggled)
        self.rbNo.toggled.connect(self.rbNo_toggled)
        self.pbSearchInvoice.clicked.connect(self.find_invoice)
        self.pbDocumentsFolder.clicked.connect(self.find_documents_folder)
        self.pbClear.clicked.connect(self.clear)
        self.pbStart.clicked.connect(self.start)

    # Initialize the elements of the window.
    def config(self):
        self.rbInvisible.setVisible(False) # Invisible button to force others to be unchecked in specific situations.
        self.rbInvisible_2.setVisible(False) # Invisible button to force others to be unchecked in specific situations.
        self.leInvoice.setReadOnly(True)
        self.leFolderPath.setReadOnly(True)

    # When "Forma de pagamento" combobox is changed:
    def payment_method_changed(self):
        if self.cbPaymentMethod.currentText() == "Boleto Agrupado":
            self.gbFirstCTe.setEnabled(True) 
            self.lbFirstCTe.setEnabled(True)
            self.rbYes.setEnabled(True) 
            self.rbNo.setEnabled(True)
            self.pbSearchInvoice.setEnabled(False)
            self.leInvoice.setEnabled(False)
            self.leInvoice.setText("")

        elif self.cbPaymentMethod.currentText() == "Boleto em Anexo":
            self.rbInvisible.setChecked(True)
            self.gbFirstCTe.setEnabled(False) 
            self.lbFirstCTe.setEnabled(False)
            self.rbYes.setEnabled(False) 
            self.rbNo.setEnabled(False)
            self.pbSearchInvoice.setEnabled(True)
            self.leInvoice.setEnabled(True)

        else:
            self.rbInvisible.setChecked(True)
            self.gbFirstCTe.setEnabled(False) 
            self.lbFirstCTe.setEnabled(False)
            self.rbYes.setEnabled(False) 
            self.rbNo.setEnabled(False)
            self.pbSearchInvoice.setEnabled(False)
            self.leInvoice.setEnabled(False)
            self.leInvoice.setText("")

    # When "Sim" button is toggled:
    def rbYes_toggled(self):
        if self.rbYes.isChecked() == True:
            self.lbFirstCTeNumber.setEnabled(True)
            self.leFirstCTeNumber.setEnabled(True)
            self.insert_first_cte = False
        else:
            self.lbFirstCTeNumber.setEnabled(False)
            self.leFirstCTeNumber.setEnabled(False)
            self.insert_first_cte = True
            self.leFirstCTeNumber.setText("")

    # When "No" button is toggled:
    def rbNo_toggled(self):
        if self.rbNo.isChecked() == True:
            self.gbInvoice.setEnabled(True)
            self.leInvoice.setEnabled(True)
            self.pbSearchInvoice.setEnabled(True)
        else:
            self.gbInvoice.setEnabled(False)
            self.leInvoice.setEnabled(False)
            self.pbSearchInvoice.setEnabled(False)
            self.leInvoice.setText("")    

    # Button to search for the invoice.
    def find_invoice(self): 
        path = QFileDialog.getOpenFileName()
        path = self.leInvoice.setText(path[0])        

    # Button to serch for the path of the "CT-e" documents.
    def find_documents_folder(self):
        path = QFileDialog.getExistingDirectory()
        path = self.leFolderPath.setText(path)

    # Store data in variables.
    def salvar_dados(self):
        if self.rbCitroen.isChecked():
            self.cnpj = "11.458.618/0001-16"
        elif self.rbJeep.isChecked():
            self.cnpj = "21.214.513/0001-75"
        elif self.rbVolkswagen.isChecked():
            self.cnpj = "03.267.961/0001-55"
        elif self.rbParque.isChecked():
            self.cnpj = "03.267.961/0004-06"
        
        self.data_vencimento = self.leDueDate.text()
        self.forma_pagamento = self.cbPaymentMethod.currentText()

        if self.forma_pagamento == "Boleto Agrupado":
            if self.rbYes.isChecked():
                self.insert_first_cte = False
            elif self.rbNo.isChecked:
                self.insert_first_cte = True
        else:
            pass
        
        self.fatura_path = self.leInvoice
        self.cte_lista = (self.pteCte.toPlainText()).split()
    
    def clear(self):
        self.rbInvisible_2.setChecked(True)
        self.rbInvisible.setChecked(True)
        self.cbPaymentMethod.setCurrentText("")
        self.leFirstCTeNumber.setText("")
        self.leDueDate.setText("")
        self.leInvoice.setText("")
        self.leFolderPath.setText("")
        self.pteCte.setPlainText("")

    def start(self):
        # Validation.
        if self.rbCitroen.isChecked() == False and self.rbJeep.isChecked() == False and self.rbVolkswagen.isChecked() == False and self.rbParque.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a unidade.")
        elif self.cbPaymentMethod.currentText() == "":
            QMessageBox.about(self, "Alerta", "Selecione a forma de pagamento.")
        elif self.cbPaymentMethod.currentText() == "Boleto Agrupado" and self.rbYes.isChecked() == False and self.rbNo.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a opção relacionada a inserção da primeira nota.")
        elif self.cbPaymentMethod.currentText() == "Boleto Agrupado" and self.rbYes.isChecked() == True and  self.leFirstCTeNumber.text() == "":
            QMessageBox.about(self, "Alerta", "Insira o número do primeiro CT-e.")
        elif self.leDueDate.text() == "//":
            QMessageBox.about(self, "Alerta", "Digite a data de vencimento.")
        elif self.cbPaymentMethod.currentText() == "Boleto Agrupado" and self.rbYes.isChecked() == True and  self.leFolderPath.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")                   
        elif self.leInvoice.text() == "" and self.rbYes.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Insira a Fatura.")
        elif self.leFolderPath.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")
        elif self.pteCte.toPlainText() == "":
            QMessageBox.about(self, "Alerta", "Digite o(s) número(s) do(s) documento(s) de CT-e.")
        else: # Create an instance of the automation code.
            self.salvar_dados()
            self.main = Main(self.user, self.password, self.cnpj, self.cbPaymentMethod.currentText(), self.insert_first_cte, self.leFirstCTeNumber.text(), self.leDueDate.text(), self.leInvoice.text(), self.leFolderPath.text(), self.cte_lista)
### End of class "main_window".