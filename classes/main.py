#Caption:
#cb: combobox
#gb: groupbox
#lb: label
#le: lineedit
#pb: pushbutton
#rb: radiobutton

from functions import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

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
        if execution == "cte number is wrong": # Stop the software if number of the file is different from its xml.
            msg = QMessageBox()
            msg.setWindowTitle("Alerta")
            msg.setText("Número de CT-e do XML está diferente do número do arquivo.") # It'll be informed on the screen.
            msg.exec_()
        
    def run(self):
        # Initialize browser.
        driver = webdriver.Edge()
        initialize(driver, self.amount_windows, self.usuario, self.senha)

        # Initialize variables.
        window_selected = -1 # There'll be an increase in the first loop.        
        last_cte = self.cte_lista[len(self.cte_lista)-1]

        # Execute a loop until every "CT-e" is in mySaga
        for cte in self.cte_lista:

            # Deal with numbers of the windows.
            if window_selected == self.amount_windows - 1:
                window_selected = 0
            else:
                window_selected+=1
            
            # Search for the xml acess key.
            chave = dados_xml(self.cte_path, cte)
            if chave == False: # If "chave" is not found, return.
                return "cte number is wrong"

            # Select window to digitalize a document.
            driver.switch_to.window(driver.window_handles[window_selected])

            # Insert "unidade" and "chave de acesso" in order to fill the fields automatically.
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
                string_unidade.clear() # Clear the field to fill in again and make sure it'll be correct.
                fill(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', self.unidade) # Typing "CNPJ".
                click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+self.unidade+"']") # Selecting "unidade"
            
            # Go to the next step.
            click(driver, 'button#tbViewDigitalizacaoNf\:btnProximoNota')
            time.sleep(0.8)

            # Payment method.
            select = Select(driver.find_element(by = By.CSS_SELECTOR, value = 'select#tbViewDigitalizacaoNf\:soFormaPagamento_input'))
            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # "Boleto agrupado" and no "CT-e" inserted.
                select.select_by_visible_text('Boleto Agrupado')

            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False: # "Boleto agrupado" and there's already "CT-e" inserted.
                select.select_by_visible_text("Boleto Agrupado")
                click(driver, 'div#tbViewDigitalizacaoNf\:sbPrimeiroBoleto') # Chang "Primeira nota?" button to "Não"

            elif self.forma_pagamento == "Boleto em Anexo": # "Boleto em anexo"
                select.select_by_visible_text("Boleto em anexo")
        
            # Check if "agência" label disappeared in order to continue.
            while True: 
                try:
                    driver.find_element(by = By.css, value = "div#tbViewDigitalizacaoNf\:j_idt415 > div:nth-child(1) > div:nth-child(3) > label[for='tbViewDigitalizacaoNf:itAgencia']")
                except:
                    break

            # Click on field "juros" and then on "CT-e" to make sure it'll be visible.
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(5)') 
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(1)')

            # Insert "CT-e" pdf.
                               
            fill(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > span > input[type=file]', self.cte_path + "/" + cte + ".pdf")
            time.sleep(0.5)
            click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

            # "Data de vencimento".
            while True:
                try:
                    driver.find_element(by = By.CSS_SELECTOR, value = 'button#tbViewDigitalizacaoNf\:accordionAnexos\:dtAnexoNotaDigitalizacao\:0\:btnVisualizaAnexoNota')
                    fill(driver, 'input#tbViewDigitalizacaoNf\:calDataVencimento_input', self.data_vencimento)
                    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
                    break
                except:
                    continue

            # Insert documento for payment or typing the first "CT-e" number.
            if self.forma_pagamento == "Boleto em Anexo" or (self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True):
                inserir_boleto(driver, self.fatura_path)
                
            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False:
                agrupar_nota(driver, self.primeiro_cte)
            
            # Go to the next step.
            click(driver, 'button#tbViewDigitalizacaoNf\:btnProximoRateio')
            time.sleep(0.5)

            # Insert "rateio".
            click(driver, 'button#tbViewDigitalizacaoNf\:btnAdicionarRateio')# "Adicionar" button.

            # Search for the departament.
            click(driver, 'label#srCentroCustoRateio_label') # Expand department list.
            time.sleep(1)
            for num in range(50): # Search for "Peças".
                centro_rateio = driver.find_element(by = By.CSS_SELECTOR, value = 'li#srCentroCustoRateio_'+str(num)).text                
                if "Peças" in centro_rateio:
                    click(driver, 'li#srCentroCustoRateio_'+str(num))
                    break
    
            time.sleep(0.5)

            # Search for the user. 
            click(driver, 'label#srUsuarioAprovador_label') # Expand user list.
            time.sleep(1)
            for num in range(30):   # Search for Pedro #srUsuarioAprovador_1
                nome_rateio = driver.find_element(by = By.CSS_SELECTOR, value = 'li#srUsuarioAprovador_'+str(num)).text
                if "PEDRO FELIPE FERREIRA LEITE" in nome_rateio:
                    click(driver, 'li#srUsuarioAprovador_'+str(num))
                    break
            time.sleep(0.5)

            # Insert value of "rateio".
            click(driver, 'input#valorRateio_input')
            fill(driver, 'input#valorRateio_input', '100') # 100% of the value.
            click(driver, 'button#btnAdicionarRateio')
            click(driver, 'button#btnSalvarSolicitacao')

            # Confirm and finish.
            while True:
                try:
                    amount_elements = driver.find_elements(by = By.CSS_SELECTOR, value = 'button#j_idt781')
                    amount_elements[-1].click() # Click on the last element of the list "amount_elements", which is the "Sim" button.
                    break
                except:
                    pass

            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # Verify if it's the first "CT-e" and awaits until it finishes loading.
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
#End of class "main".