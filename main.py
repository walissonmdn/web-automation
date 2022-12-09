#Caption:
#cb: combobox
#gb: groupbox
#lb: label
#le: lineedit
#pb: pushbutton
#rb: radiobutton

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from functions import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

class login(QMainWindow): # Login Screen
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("login_window.ui", self)
        self.show()
        self.pbLogin.clicked.connect(self.check)
    
    def check(self):
        # Validation
        if self.leLogin.text() == "":
            QMessageBox.about(self, "Alerta", "Digite o usuário", )
        
        elif self.leSenha.text() == "":
            QMessageBox.about(self, "Alerta", "Digite a senha", )
        # Create an instance of main_windows
        else:
            self.close()
            self.windows_main = main_window(self.leLogin.text(), self.leSenha.text())
### End of class.

class main_window(QMainWindow):   # Fill in the necessary data of a "CT-e"
    def __init__(self, usuario, senha):
        super(main_window, self).__init__()
        uic.loadUi("main_window.ui", self)
        self.usuario = usuario
        self.senha = senha
        self.inserir_primeiro_cte = False
        self.config()
        self.show()
        self.cbFormadePagamento.currentTextChanged.connect(self.forma_pagamento_changed) # Chama função quando combobox for alterado
        self.rbSim.toggled.connect(self.rbSim_toggled) # Primeira nota já foi inserida, logo não vai ter boleto
        self.rbNao.toggled.connect(self.rbNao_toggled)
        self.pbProcurarFatura.clicked.connect(self.encontrar_fatura)
        self.pbLocalizacaoCte.clicked.connect(self.encontrar_pasta_cte)
        self.pbLimpar.clicked.connect(self.limpar)
        self.pbIniciar.clicked.connect(self.iniciar)

    # Initializing the elements of the window.
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

    # Storing data in variables.
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
### End of class.

class main(QMainWindow): # Class to represent the automation code and its settings.
    def __init__(self, usuario, senha, unidade, forma_pagamento, inserir_primeiro_cte, primeiro_cte, data_vencimento, fatura_path, cte_path, cte_lista):
        self.usuario = usuario
        self.senha = senha
        self.unidade = unidade
        self.forma_pagamento = forma_pagamento
        self.inserir_primeiro_cte = inserir_primeiro_cte
        self.data_vencimento = data_vencimento
        self.fatura_path = fatura_path
        self.cte_path = cte_path
        self.cte_lista = cte_lista
        
        # If the first "CT-e" is already in the system, specify its number. Otherwise, the number will be the first "CT-e"'s inserted.
        if inserir_primeiro_cte == True:
            self.primeiro_cte = self.cte_lista[0]
        else:
            self.primeiro_cte = primeiro_cte

        # The amount of tabs that'll be opened.
        if len(self.cte_lista) < 5:
            self.amount_windows = len(self.cte_lista)
        else:
            self.amount_windows = 5 # If there are more than 5 "CT-e" documents, only 5 tabs will be opened.
        
        # It calls the function to execute the automation code.
        execution = self.run()
        if execution == "cte number is wrong": # Parar o programa caso o arquivo de CT-e esteja com o número diferente do xml.
            msg = QMessageBox()
            msg.setWindowTitle("Alerta")
            msg.setText("Número de CT-e do XML está diferente do número do arquivo.") # Será informado na tela do usuário.
            msg.exec_()
        
    def run(self):
        # Initializing browser.
        driver = webdriver.Edge()
        initialize(driver, self.amount_windows, self.usuario, self.senha)

        # Initializing variables.
        window_selected = -1 # There'll be an increase in the first loop.
        repeticao_pagina = 1 # Necessary variable, since button to a confirmation popup has its index changed each "CT-e" inserted.
        
        last_cte = self.cte_lista[len(self.cte_lista)-1]

        # Executing a loop until every "CT-e" is in mySaga
        for cte in self.cte_lista:

            # Dealing with windows numbers.
            if window_selected == self.amount_windows - 1:
                window_selected = 0
                repeticao_pagina+=1 # Index inicial do botão é igual a 1
            else:
                window_selected+=1
            
            # Searching for the xml acess key.
            chave = dados_xml(self.cte_path, cte)
            if chave == False: # Função de cima retorna False caso núm de CT-e no xml esteja diferente do arquivo salvo.
                return "cte number is wrong"

            # Selecting window to digitalize a document.
            driver.switch_to.window(driver.window_handles[window_selected])

            # Inserting "unidade" and "chave de acesso" in order to fill the fields automatically.
            click(driver, 'button#btnCriarPedido')
            click(driver, 'table#opcoesDigitalizacao > tbody > tr > td:nth-child(4) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default')
            fill(driver, 'input#itUnidadeCteDigitalizacao_input', self.unidade)
            click(driver, "span#itUnidadeCteDigitalizacao_panel > table > tbody > tr[data-item-label*='"+self.unidade+"']")
            time.sleep(0.5)
            fill(driver, 'input#itChaveCteDigitalizacao', chave)
            click(driver, 'button#btnEnviarCaptchaCteInformar')

            # Checking if "unidade" is already filled and if so, it checks if it's correct.
            click(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input')
            string_unidade = driver.find_element(by = By.CSS_SELECTOR, value = 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input')
            if self.unidade in string_unidade.get_attribute("value"):
                pass
            else:
                string_unidade.clear() # Clearing the field to fill in again and make sure it'll be correct.
                fill(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', self.unidade) # Typing "CNPJ".
                                        #tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr
                click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+self.unidade+"']") # Selecting "unidade"
            # Going to the next step.
            click(driver, 'button#tbViewDigitalizacaoNf\:btnProximoNota')
            time.sleep(0.8)

            # Payment method.
            select = Select(driver.find_element(by = By.CSS_SELECTOR, value = 'select#tbViewDigitalizacaoNf\:soFormaPagamento_input'))
            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # "Boleto agrupado" and no "CT-e" inserted.
                select.select_by_visible_text('Boleto Agrupado')

            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False: # "Boleto agrupado" and there's already "CT-e" inserted.
                select.select_by_visible_text("Boleto Agrupado")
                click(driver, 'div#tbViewDigitalizacaoNf\:sbPrimeiroBoleto') # Changing "Primeira nota?" button to "Não"

            elif self.forma_pagamento == "Boleto em Anexo": # "Boleto em anexo"
                select.select_by_visible_text("Boleto em anexo")
        
            # Checking if "agência" label disappeared in order to continue.
            while True: 
                try:
                    driver.find_element(by = By.css, value = "div#tbViewDigitalizacaoNf\:j_idt415 > div:nth-child(1) > div:nth-child(3) > label[for='tbViewDigitalizacaoNf:itAgencia']")
                except:
                    break

            # Clicking on field "juros" and then on "CT-e" to make sure it'll be visible.
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(5)') 
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(1)')

            # Inserting "CT-e" pdf.
            fill(driver, 'input#tbViewDigitalizacaoNf\:accordionAnexos\:j_idt465_input', self.cte_path + "/" + cte + ".pdf")
            time.sleep(0.5)
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:j_idt465 > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

            # "Data de vencimento".
            while True:
                try:
                    driver.find_element(by = By.CSS_SELECTOR, value = 'button#tbViewDigitalizacaoNf\:accordionAnexos\:dtAnexoNotaDigitalizacao\:0\:btnVisualizaAnexoNota')
                    fill(driver, 'input#tbViewDigitalizacaoNf\:calDataVencimento_input', self.data_vencimento)
                    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
                    break
                except:
                    continue

            # Inserting documento for payment or typing the first "CT-e" number.
            if self.forma_pagamento == "Boleto em Anexo" or (self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True):
                inserir_boleto(driver, self.fatura_path)
                
            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False:
                agrupar_nota(driver, self.primeiro_cte, repeticao_pagina)
            
            # Going to the next step.
            click(driver, 'button#tbViewDigitalizacaoNf\:btnProximoRateio')
            time.sleep(0.5)

            # Inserting "rateio".
            click(driver, 'button#tbViewDigitalizacaoNf\:btnAdicionarRateio')# "Adicionar" button.

            # Searching for the departament.
            click(driver, 'label#srCentroCustoRateio_label') # Expanding department list.
            time.sleep(1)
            for num in range(50): # Search for "Peças".
                centro_rateio = driver.find_element(by = By.CSS_SELECTOR, value = 'li#srCentroCustoRateio_'+str(num)).text                
                if "Peças" in centro_rateio:
                    click(driver, 'li#srCentroCustoRateio_'+str(num))
                    break
    
            time.sleep(0.5)

            # Searching for the user. 
            click(driver, 'label#srUsuarioAprovador_label') # Expanding user list.
            time.sleep(1)
            for num in range(30):   # Search for Pedro #srUsuarioAprovador_1
                nome_rateio = driver.find_element(by = By.CSS_SELECTOR, value = 'li#srUsuarioAprovador_'+str(num)).text
                if "PEDRO FELIPE FERREIRA LEITE" in nome_rateio:
                    click(driver, 'li#srUsuarioAprovador_'+str(num))
                    break
            time.sleep(0.5)

            # Inserting value of "rateio".
            click(driver, 'input#valorRateio_input')
            fill(driver, 'input#valorRateio_input', '100') # 100% of the value.
            click(driver, 'button#btnAdicionarRateio')
            click(driver, 'button#btnSalvarSolicitacao')

            # Confirming and finishing.
            while True:
                try:
                    amount_elements = driver.find_elements(by = By.CSS_SELECTOR, value = 'button#j_idt782')
                    amount_elements[-1].click() # Clicking on the last element of the list "amount_elements", which is the "Sim" button.
                    break
                except:
                    pass

            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # Verifying if it's the first "CT-e" and awaits until it finishes loading.
                self.inserir_primeiro_cte = False
                while True:
                    try:
                        click(driver, '#btnCriarPedido')
                        driver.refresh()
                        break
                    except:
                        pass
            elif cte == last_cte: # Awaits until the last "CT-e" insertion is finished to finish the browser.
                while True:
                    try:
                        click(driver, '#btnCriarPedido')
                        break
                    except:
                        pass
#End of class.

#Execute the software.
app = QApplication(sys.argv)
login_window = login() # Making an instance from login class.
app.exec_()


