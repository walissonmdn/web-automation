from functions.selenium_functions import *
from functions.general_functions import *
import time

def inserir_boleto(driver, invoice_path):
    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
    click(driver, 'button#tbViewDigitalizacaoNf\:accordionAnexos\:dtBoletoDigitalizacao\:0\:btnAdicionaBoleto')
    fill(driver, 'input#fileUploadBoleto_input', invoice_path)
    click(driver, 'div#fileUploadBoleto > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

def agrupar_nota(driver, first_cte_number):
    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
    time.sleep(0.5)
    while True:
        try:
            first_cte_field = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:j_idt502\:filter")
            selenium_send_keys(first_cte_field, first_cte_number)
            break
        except:
            try:
                first_cte_field = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:j_idt588\:filter")
                selenium_send_keys(first_cte_field, first_cte_number)
                break
            except:
                pass
    
    time.sleep(0.5)
    while True:
        try:
            selenium_click(selenium_find_element(driver, "button#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:0\:j_idt511"))
            break
        except:
            try:
                selenium_click(selenium_find_element(driver, "button#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:0\:j_idt602"))
                break
            except:
                pass
    time.sleep(0.5)

    while True:
        try:
            amount_elements = selenium_find_elements(driver, "button#j_idt789") 
            selenium_click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
            break
        except:
            try:
                amount_elements = selenium_find_elements(driver, "button#j_idt1037") 
                selenium_click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                break 
            except:
                pass


def fill_invoice_data(driver, payment_method, insert_first_cte, due_date, invoice_path, first_cte_number, documents_path, cte):
    # Payment method.
                payment = selenium_select(selenium_find_element(driver, "select#tbViewDigitalizacaoNf\:soFormaPagamento_input")) 
                if payment_method == "Boleto Agrupado" and insert_first_cte == True: # "Boleto agrupado" and no "CT-e" inserted.
                    selenium_select_by_visible_text(payment, "Boleto Agrupado")

                elif payment_method == "Boleto Agrupado" and insert_first_cte == False: # "Boleto agrupado" and there's already "CT-e" inserted.
                    selenium_select_by_visible_text(payment, "Boleto Agrupado")
                    click(driver, 'div#tbViewDigitalizacaoNf\:sbPrimeiroBoleto') # Change "Primeira nota?" button to "Não"

                elif payment_method == "Boleto em Anexo": # "Boleto em anexo"
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
                                
                fill(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > span > input[type=file]', documents_path + "/" + cte + ".pdf")
                time.sleep(0.5)
                click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

                # "Data de vencimento".
                while True:
                    try:
                        selenium_find_element(driver, "button#tbViewDigitalizacaoNf\:accordionAnexos\:dtAnexoNotaDigitalizacao\:0\:btnVisualizaAnexoNota")
                        fill(driver, "input#tbViewDigitalizacaoNf\:calDataVencimento_input", due_date)
                        click(driver, "div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)")
                        break
                    except:
                        continue

                # Insert documento for payment or typing the first "CT-e" number.
                if payment_method == "Boleto em Anexo" or (payment_method == "Boleto Agrupado" and insert_first_cte == True):
                    inserir_boleto(driver, invoice_path)
                    
                elif payment_method == "Boleto Agrupado" and insert_first_cte == False:
                    agrupar_nota(driver, first_cte_number)
                
                # Go to the next step.
                click(driver, "button#tbViewDigitalizacaoNf\:btnProximoRateio")
                time.sleep(0.5)