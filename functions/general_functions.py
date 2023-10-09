from functions.selenium_functions import *
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from xml.dom import minidom

def click(driver, css_selector): # Click on the specified element.
    while True:
        try:
            driver.find_element(by = By.CSS_SELECTOR, value = css_selector).click()
            break
        except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, AttributeError):
            pass


def fill(driver, css_selector, text): # Fill in a field or upload a file.
    while True:
        try:
            driver.find_element(by = By.CSS_SELECTOR, value = css_selector).send_keys(text)
            break
        except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, AttributeError):
            pass
        
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
                amount_elements = selenium_find_elements(driver, "button#j_idt787") 
                selenium_click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                break 
            except:
                pass
           # try:

            #except:
            #    pass

def digitalizacao_automatica_cte(driver, unidade):
    # Check if "Unidade" has any value and if it's correct.
    string_unidade = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input")

    if unidade in string_unidade.get_attribute("value"):
        pass
    else:
        selenium_clear(string_unidade) # Clear the field to fill in again and make sure it'll be correct.
        selenium_send_keys(string_unidade, unidade)
        click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+unidade+"']") # Select "unidade".
    
    # Check whether "Serviço/Produto" is already selected and if so, it checks if it's correct.
    while True:
        try:
            string_servico = selenium_get_text(selenium_find_element(driver, "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label"))
            break
        except StaleElementReferenceException:
            pass

    if "frete" in string_servico.lower():
        pass
    else:
        try:
            for num in range(5):
                servico = selenium_get_text(selenium_find_element(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                if "frete" in servico.lower():
                    click(driver, "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
                    click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                    break
        except:
            click(driver, "button#tbViewDigitalizacaoNf\:btnBuscarFornecedor")
            click(driver, "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
            time.sleep(1)
            try:
                for num in range(5):
                    servico = selenium_get_text(selenium_find_element(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                    if "frete" in servico.lower():
                        click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                        break
            except:
                for num in range(5):
                    servico = selenium_get_text(selenium_find_element(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                    if "não cadastrado" in servico.lower():
                        click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                        break

    click(driver, "button#tbViewDigitalizacaoNf\:btnProximoNota")
    time.sleep(0.8)


def digitalizacao_manual_cte(driver, cte, unidade, dados_xml):
    click(driver, "button#j_idt719")
    fill(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', unidade)
    click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+unidade+"']")
    click(driver, "table#tbViewDigitalizacaoNf\:srTipoNota > tbody > tr > td:nth-child(1) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default")
    fill(driver, "input#tbViewDigitalizacaoNf\:itChaveNota", dados_xml[0]+Keys.TAB)
    time.sleep(1)

    #Type the value of the "CT-e"
    valor = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itValorNota")
    selenium_clear(valor)
    time.sleep(0.5)
    selenium_send_keys(valor, dados_xml[1])
    time.sleep(0.5)
    fill(driver, "input#tbViewDigitalizacaoNf\:itCnpjFornecedor", dados_xml[2]) 
    click(driver, "button#tbViewDigitalizacaoNf\:btnBuscarFornecedor")
    time.sleep(0.5)
    fill(driver, "input#tbViewDigitalizacaoNf\:itNumeroNota", cte)
    time.sleep(0.5)
    fill(driver, "input#tbViewDigitalizacaoNf\:itNumeroSerie", dados_xml[3])
    time.sleep(0.5)
    fill(driver, "input#tbViewDigitalizacaoNf\:calDataEmissao_input", dados_xml[4]+Keys.TAB)
    time.sleep(0.5)

    click(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao")
    fill(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao", "Frete"+Keys.TAB)

    #Select "Serviço/Produto"
    exit_loop = False
    while True:
        try:
            selenium_find_element(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_1")
            click(driver, "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
            time.sleep(0.5)
            while True:
                try:
                    for num in range(5):
                        servico = selenium_get_text(selenium_find_element(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                        if ("frete" in servico.lower()) or ("não cadastrado" in servico.lower()):
                            click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                            exit_loop = True
                            break
                
                    if exit_loop == True:
                        while True:
                            try:
                                selenium_click(selenium_find_element(driver, "button#tbViewDigitalizacaoNf\:btnProximoNota"))
                                break
                            except:
                                try:
                                    valor = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itValorNota")
                                    selenium_clear(valor)
                                    time.sleep(0.5)
                                    selenium_send_keys(valor, dados_xml[1])
                                    time.sleep(0.5)

                                    num_cte = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itNumeroNota")
                                    selenium_clear(num_cte)
                                    time.sleep(0.5)
                                    selenium_send_keys(num_cte, cte)
                                    time.sleep(0.5)
                                    click(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao")

                                    num_serie = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itNumeroSerie")
                                    selenium_clear(num_serie)
                                    time.sleep(0.5)
                                    selenium_send_keys(num_serie, dados_xml[3])
                                    time.sleep(0.5)
                                    click(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao")

                                    data_emissao = selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:calDataEmissao_input")
                                    selenium_clear(data_emissao)
                                    time.sleep(0.5)
                                    selenium_send_keys(data_emissao, dados_xml[4]+Keys.TAB)
                                    time.sleep(0.5)
                                    click(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao")
                                except:
                                    pass

                        time.sleep(0.8)
                        break
                except:
                    pass
            if exit_loop == True:
                break

        except:
            try:
                selenium_click(selenium_find_element(driver,"button#tbViewDigitalizacaoNf\:btnProximoNota"))
                time.sleep(0.8)
                break
            except:
                pass

    

def read_xml(cte_path, cte): # Read xml.
    xml = open(cte_path + "/" + cte + ".xml")
    cte_parse = minidom.parse(xml)
    cte_num = cte_parse.getElementsByTagName("nCT")
    cte_num = (cte_num[0].firstChild.data)

    # Check whether the xml file number is the same as the information in it.
    if cte == cte_num:
        chave = cte_parse.getElementsByTagName("chCTe")
        chave = (chave[-1].firstChild.data)
    else:
        chave = False

    valor_cte = cte_parse.getElementsByTagName('vRec')
    valor_cte = valor_cte[0].firstChild.data

    cnpj = cte_parse.getElementsByTagName("CNPJ")
    cnpj = cnpj[0].firstChild.data

    serie = cte_parse.getElementsByTagName("serie")
    serie = serie[0].firstChild.data

    # Busca pela data de emissão
    data_emissao = cte_parse.getElementsByTagName('dhEmi')
    data_emissao = (data_emissao[0].firstChild.data)
    #yyyy-mm-dd to dd-mm-yyyy
    data_emissao = data_emissao[8] + data_emissao[9] + '/' + data_emissao[5] + data_emissao[6] + '/' + data_emissao[0] + data_emissao[1] + data_emissao[2] + data_emissao[3]

    return [chave, valor_cte, cnpj, serie, data_emissao]