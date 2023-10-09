# Contractions:
# cb: combobox
# gb: groupbox
# lb: label
# le: lineedit
# pb: pushbutton
# rb: radiobutton

#from functions.general_functions import *
from src.selenium import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
import time
import urllib3.exceptions
from src.webpages.login_page import *
from src.webpages.digitalization_page import *
from src.extract_data_xml import *

class Main(QMainWindow): # Class to represent the automation code and its settings.
    def __init__(self, user, password, legal_person_number, payment_method, insert_first_cte, first_cte_number, due_date, invoice_path, documents_path, documents_numbers_list):
        self.user = user
        self.password = password
        self.legal_person_number = legal_person_number
        self.payment_method = payment_method
        self.insert_first_cte = insert_first_cte
        self.due_date = due_date
        self.invoice_path = invoice_path
        self.documents_path = documents_path
        self.documents_numbers_list = documents_numbers_list
        
        # If the first "CT-e" is already in the system, specify its number. Otherwise, the number will be the first "CT-e"'s inserted.
        if insert_first_cte == True:
            self.first_cte_number = self.documents_numbers_list[0].lstrip('0')
        else:
            self.first_cte_number = first_cte_number.lstrip('0')

        # The amount of tabs that'll be opened.
        if len(self.documents_numbers_list) < 5:
            self.amount_windows = len(self.documents_numbers_list)
        else:
            self.amount_windows = 5 # If there are more than 5 "CT-e" documents, only 5 tabs will be opened.
        
        # It calls the function to execute the automation code.
        execution = self.run()
        status = execution
        if execution == "Completed.":
            msg = QMessageBox()
            msg.setWindowTitle("Alerta!")
            msg.setText(status) # It'll be informed on the screen.
            msg.exec_()
        elif execution == "File number is different from the xml tree.":
            msg = QMessageBox()
            msg.setWindowTitle("Alerta!")
            msg.setText(status) # It'll be informed on the screen.
            msg.exec_()
        elif execution == "Failure to communicate with the browser.":
            msg = QMessageBox()
            msg.setWindowTitle("Atenção!")
            msg.setText(status) # It'll be informed on the screen.
            msg.exec_()
        
    def run(self):
        try:
            driver = Selenium()
        
            login_page = LoginPage(driver, self.user, self.password)
            login_page.login()

            # Await until login is completed.
            driver.wait_for_element_to_appear("span.ui-menuitem-text")

            digitalization_page = DigitalizationPage(driver, self.legal_person_number)
            digitalization_page.get_digitalization_page()
            digitalization_page.open_multiple_tabs(self.amount_windows)

            window_index = -1 # There'll be an increase in the first loop.        

            for document_number in self.documents_numbers_list:
                document_number = document_number.lstrip('0')

                digitalization_page.switch_tabs(self.amount_windows, window_index)
            
                xml_file = XMLDataExtractor(document_number, self.documents_path)
                xml_data = xml_file.extract_data()

                if xml_data["document_number"] != document_number: 
                    return "File number is different from the xml tree."

                digitalization_page.find_document_automatically(xml_data)

                document_has_been_found = digitalization_page.check_if_document_has_been_found()
                if document_has_been_found == True: 
                    digitalization_page.check_form(self.legal_person_number)
                else:
                    digitalization_page.fill_in_form(document_number, self.legal_person_number, xml_data)

                digitalization_page.select_payment_method(self.payment_method, self.insert_first_cte)
                # Make sure payment method change has been completed.
                driver.wait_for_element_to_disappear("div#tbViewDigitalizacaoNf\:j_idt415 > div:nth-child(1) > div:nth-child(3) > label[for='tbViewDigitalizacaoNf:itAgencia']")
                
                # Click on field "juros" and then on "CT-e" to make sure it'll be visible.
                driver.click_loop("div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(5)") 
                driver.click_loop("div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(1)")

                digitalization_page.upload_document(self.documents_path, document_number)

                digitalization_page.fill_in_due_date(self.due_date)

                if self.payment_method == "Boleto em Anexo" or (self.payment_method == "Boleto Agrupado" and self.insert_first_cte == True):
                    digitalization_page.upload_invoice(self.invoice_path)
                    
                elif self.payment_method == "Boleto Agrupado" and self.insert_first_cte == False:
                    digitalization_page.relate_documents(self.first_cte_number)

                # Go to the next step.
                driver.click_loop("button#tbViewDigitalizacaoNf\:btnProximoRateio")
                time.sleep(0.5)

                digitalization_page.insert_payer()

                digitalization_page.save()

                if self.payment_method == "Boleto Agrupado" and self.insert_first_cte == True:
                    self.insert_first_cte = False
                    digitalization_page.await_unitl_first_digitalization_finishes()

                elif document_number == self.documents_numbers_list[len(self.documents_numbers_list)-1]: # Awaits until the last "CT-e" insertion is finished to finish the browser.
                    digitalization_page.await_until_last_digitalization_finishes()

                print("ok")
                
        except (NoSuchWindowException, WebDriverException, urllib3.exceptions.ProtocolError):
            error = "Failure to communicate with the browser." 
            return error
            