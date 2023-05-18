# Contractions:
# cb: combobox
# gb: groupbox
# lb: label
# le: lineedit
# pb: pushbutton
# rb: radiobutton

from functions.general_functions import *
from functions.selenium_functions import *
from functions.window_dados import *
from functions.window_documentos import *
from functions.window_rateio import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import time

class main(QMainWindow): # Class to represent the automation code and its settings.
    def __init__(self, user, password, cnpj, payment_method, insert_first_cte, first_cte_number, due_date, invoice_path, documents_path, cte_list):
        self.user = user
        self.password = password
        self.cnpj = cnpj
        self.payment_method = payment_method
        self.insert_first_cte = insert_first_cte
        self.due_date = due_date
        self.invoice_path = invoice_path
        self.documents_path = documents_path
        self.cte_list = cte_list
        
        # If the first "CT-e" is already in the system, specify its number. Otherwise, the number will be the first "CT-e"'s inserted.
        if insert_first_cte == True:
            self.first_cte_number = self.cte_list[0]
        else:
            self.first_cte_number = first_cte_number

        # The amount of tabs that'll be opened.
        if len(self.cte_list) < 5:
            self.amount_windows = len(self.cte_list)
        else:
            self.amount_windows = 5 # If there are more than 5 "CT-e" documents, only 5 tabs will be opened.
        
        # It calls the function to execute the automation code.
        execution = self.run()
        error = execution
        if execution == "Número do arquivo de CT-e está diferente do número na árvore do XML.":
            msg = QMessageBox()
            msg.setWindowTitle("Alerta!")
            msg.setText(error) # It'll be informed on the screen.
            msg.exec_()
        elif execution == "O navegador foi encerrado pelo usuário":
            msg = QMessageBox()
            msg.setWindowTitle("Atenção!")
            msg.setText(error) # It'll be informed on the screen.
            msg.exec_()
        
    def run(self):
        try:
            # Initialize browser.
            driver = webdriver.Edge()
            initialize(driver, self.amount_windows, self.user, self.password)

            # Initialize variables.
            window_selected = -1 # There'll be an increase in the first loop.        
            last_cte = self.cte_list[len(self.cte_list)-1]

            # Execute a loop until every "CT-e" is in mySaga.
            for cte in self.cte_list:

                # Deal with numbers of the windows.
                if window_selected == self.amount_windows - 1:
                    window_selected = 0
                else:
                    window_selected+=1                

                # Select window to digitalize a document.
                driver.switch_to.window(driver.window_handles[window_selected])

                # Search for the xml acess key.
                dados_xml = read_xml(self.documents_path, cte)
                if dados_xml[0] == False: # If "chave" is not found, return.
                    error = "Número do arquivo de CT-e está diferente do número na árvore do XML."
                    return error

                # Insert "unidade" and "chave de acesso" in order to try to fill the fields automatically.
                click(driver, 'button#btnCriarPedido')
                click(driver, 'table#opcoesDigitalizacao > tbody > tr > td:nth-child(4) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default')
                fill(driver, 'input#itUnidadeCteDigitalizacao_input', self.cnpj)
                click(driver, "span#itUnidadeCteDigitalizacao_panel > table > tbody > tr[data-item-label*='"+self.cnpj+"']")
                time.sleep(0.5)
                fill(driver, 'input#itChaveCteDigitalizacao', dados_xml[0])
                click(driver, 'button#btnEnviarCaptchaCteInformar')

                # (First Step) Part of the screen: "Dados"
                fill_cte_data(driver, cte, self.cnpj, dados_xml)
                
                # (Second Step) Part of the screen: "Documentos"
                fill_invoice_data(driver, self.payment_method, self.insert_first_cte, self.due_date, self.invoice_path, self.first_cte_number, self.documents_path, cte)

               # (Third Step) Part of the screen: "Rateio"
                fill_department(driver)

                
                if self.payment_method == "Boleto Agrupado" and self.insert_first_cte == True: # Verify if it's the first "CT-e" and awaits until it finishes loading.
                    self.insert_first_cte = False
                    while True:
                        try:
                            click(driver, "#btnCriarPedido")
                            selenium_refresh(driver)
                            break
                        except:
                            pass
                elif cte == last_cte: # Awaits until the last "CT-e" insertion is finished to finish the browser.
                    while True:
                        try:
                            click(driver, "#btnCriarPedido")
                            break
                        except:
                            pass
        except NoSuchWindowException:
            error = "O navegador foi encerrado pelo usuário." 
            return error
#End of class "main".