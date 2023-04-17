# Contractions:
# cb: combobox
# gb: groupbox
# lb: label
# le: lineedit
# pb: pushbutton
# rb: radiobutton

from functions.general_functions import *
from functions.selenium_functions import *
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

                # Insert "unidade" and "chave de acesso" in order to fill the fields automatically.
                click(driver, 'button#btnCriarPedido')
                click(driver, 'table#opcoesDigitalizacao > tbody > tr > td:nth-child(4) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default')
                fill(driver, 'input#itUnidadeCteDigitalizacao_input', self.cnpj)
                click(driver, "span#itUnidadeCteDigitalizacao_panel > table > tbody > tr[data-item-label*='"+self.cnpj+"']")
                time.sleep(0.5)
                fill(driver, 'input#itChaveCteDigitalizacao', dados_xml[0])
                click(driver, 'button#btnEnviarCaptchaCteInformar')

                while True:
                    try:
                        selenium_click(selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itNumeroNota")) # Verify whether the "CT-e" was imported automatically. 
                        digitalizacao_automatica_cte(driver, self.cnpj)
                        break
                    except:
                        try:
                            selenium_click(selenium_find_element(driver, "button#btnCriarPedido"))
                            digitalizacao_manual_cte(driver, cte, self.cnpj, dados_xml)
                            break
                        except:
                            pass
                
                # Go to the next step.
                click(driver, 'button#tbViewDigitalizacaoNf\:btnProximoNota')
                time.sleep(0.8)

                # Payment method.
                payment = selenium_select(selenium_find_element(driver, "select#tbViewDigitalizacaoNf\:soFormaPagamento_input")) 
                if self.payment_method == "Boleto Agrupado" and self.insert_first_cte == True: # "Boleto agrupado" and no "CT-e" inserted.
                    selenium_select_by_visible_text(payment, "Boleto Agrupado")

                elif self.payment_method == "Boleto Agrupado" and self.insert_first_cte == False: # "Boleto agrupado" and there's already "CT-e" inserted.
                    selenium_select_by_visible_text(payment, "Boleto Agrupado")
                    click(driver, 'div#tbViewDigitalizacaoNf\:sbPrimeiroBoleto') # Change "Primeira nota?" button to "Não"

                elif self.payment_method == "Boleto em Anexo": # "Boleto em anexo"
                    selenium_select_by_visible_text(payment, "Boleto em anexo")
            
                # Check if "agência" label disappeared in order to continue.
                while True: 
                    try:
                        selenium_find_element(driver, "div#tbViewDigitalizacaoNf\:j_idt415 > div:nth-child(1) > div:nth-child(3) > label[for='tbViewDigitalizacaoNf:itAgencia']")
                    except:
                        break

                # Click on field "juros" and then on "CT-e" to make sure it'll be visible.
                click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(5)') 
                click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(1)')

                # Insert "CT-e" pdf.
                                
                fill(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > span > input[type=file]', self.documents_path + "/" + cte + ".pdf")
                time.sleep(0.5)
                click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

                # "Data de vencimento".
                while True:
                    try:
                        selenium_find_element(driver, "button#tbViewDigitalizacaoNf\:accordionAnexos\:dtAnexoNotaDigitalizacao\:0\:btnVisualizaAnexoNota")
                        fill(driver, "input#tbViewDigitalizacaoNf\:calDataVencimento_input", self.due_date)
                        click(driver, "div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)")
                        break
                    except:
                        continue

                # Insert documento for payment or typing the first "CT-e" number.
                if self.payment_method == "Boleto em Anexo" or (self.payment_method == "Boleto Agrupado" and self.insert_first_cte == True):
                    inserir_boleto(driver, self.invoice_path)
                    
                elif self.payment_method == "Boleto Agrupado" and self.insert_first_cte == False:
                    agrupar_nota(driver, self.first_cte_number)
                
                # Go to the next step.
                click(driver, "button#tbViewDigitalizacaoNf\:btnProximoRateio")
                time.sleep(0.5)

                # Insert "rateio".
                click(driver, "button#tbViewDigitalizacaoNf\:btnAdicionarRateio")# "Adicionar" button.

                # Search for the departament.
                click(driver, "label#srCentroCustoRateio_label") # Expand department list.
                time.sleep(1)
                for num in range(50): # Search for "Peças".
                    centro_rateio = selenium_get_text(selenium_find_element(driver, "li#srCentroCustoRateio_"+str(num)))
                    if "Peças" in centro_rateio:
                        click(driver, "li#srCentroCustoRateio_"+str(num))
                        break
        
                time.sleep(0.5)

                # Search for the user. 
                click(driver, "label#srUsuarioAprovador_label") # Expand user list.
                time.sleep(1)
                for num in range(30):   # Search for Pedro #srUsuarioAprovador_1
                    nome_rateio = selenium_get_text(selenium_find_element(driver, "li#srUsuarioAprovador_"+str(num)))
                    if "PEDRO FELIPE FERREIRA LEITE" in nome_rateio:
                        click(driver, "li#srUsuarioAprovador_"+str(num))
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
                        amount_elements = selenium_find_elements(driver, "button#j_idt789")
                        selenium_click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                        break
                    except:
                        pass

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