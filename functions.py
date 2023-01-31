from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from xml.dom import minidom

def initialize(driver, amount_windows, usuario, senha): # Initialize browser.
    driver.get("https://mysaga.gruposaga.com.br/public/index.jsf")
    fill(driver, 'input#saga_username', usuario)
    fill(driver, 'input#saga_password', senha)
    click(driver, 'input#btnLoginId')
    driver.get("https://mysaga.gruposaga.com.br/sistema/CSC/digitalizacaoNf/digitalizacaoNF.jsf?faces-redirect=true")
    if amount_windows > 1:
        open = 0
        while open < amount_windows - 1:
            driver.execute_script("window.open('https://mysaga.gruposaga.com.br/sistema/CSC/digitalizacaoNf/digitalizacaoNF.jsf?faces-redirect=true');")
            open+=1

def click(driver, css_selector): # Click on the specified element.
    while True:
        try:
            driver.find_element(by = By.CSS_SELECTOR, value = css_selector).click()
            break
        except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException):
            pass


def fill(driver, css_selector, text): # Fill in a field or upload a file.
    while True:
        try:
            driver.find_element(by = By.CSS_SELECTOR, value = css_selector).send_keys(text)
            break
        except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
            pass

def inserir_boleto(driver, fatura_path):
    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
    click(driver, 'button#tbViewDigitalizacaoNf\:accordionAnexos\:dtBoletoDigitalizacao\:0\:btnAdicionaBoleto')
    fill(driver, 'input#fileUploadBoleto_input', fatura_path)
    click(driver, 'div#fileUploadBoleto > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

def agrupar_nota(driver, primeiro_cte):
    click(driver, 'div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
    time.sleep(0.5)
    fill(driver, 'input#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:j_idt502\:filter', primeiro_cte)
    time.sleep(0.5)
    click(driver, 'button#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:0\:j_idt511')
    time.sleep(0.5)

    while True:
        try:
            amount_elements = driver.find_elements(by = By.CSS_SELECTOR, value = 'button#j_idt789')
            amount_elements[-1].click() # Click on the list item of amount_elements list, which is the "Sim" button.
            break
        except:
            pass

def digitalizacao_automatica_cte(driver, unidade):
    string_unidade = driver.find_element(by = By.CSS_SELECTOR, value = 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input')
    if unidade in string_unidade.get_attribute("value"):
        pass
    else:
        string_unidade.clear() # Clear the field to fill in again and make sure it'll be correct.
        string_unidade.send_keys(unidade)
        #fill(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', unidade) # Typing "CNPJ".
        click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+unidade+"']") # Selecting "unidade"
    
    #Check whether "Serviço/Produto" is already selected and if so, it checks if it's correct.
    while True:
        try:
            string_servico = driver.find_element(by = By.CSS_SELECTOR, value = "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label").text
            break
        except StaleElementReferenceException:
            pass

    if "frete" in string_servico.lower():
        pass
    else:
        try:
            for num in range(5):
                servico = driver.find_element(by = By.CSS_SELECTOR, value = "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)).text
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
                    servico = driver.find_element(by = By.CSS_SELECTOR, value = "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)).text
                    if "frete" in servico.lower():
                        click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                        break
            except:
                for num in range(5):
                    servico = driver.find_element(by = By.CSS_SELECTOR, value = "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)).text
                    if "não cadastrado" in servico.lower():
                        click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                        break


def digitalizacao_manual_cte(driver, cte, unidade, dados_xml):
    click(driver, "button#j_idt717")
    fill(driver, 'input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', unidade)
    click(driver, "span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+unidade+"']")
    click(driver, "table#tbViewDigitalizacaoNf\:srTipoNota > tbody > tr > td:nth-child(1) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default")
    fill(driver, "input#tbViewDigitalizacaoNf\:itChaveNota", dados_xml[0]+Keys.TAB)
    time.sleep(0.5)

    #Type the value of the "CT-e"
    valor = driver.find_element(by = By.CSS_SELECTOR, value = "input#tbViewDigitalizacaoNf\:itValorNota")
    valor.clear()
    valor.send_keys(dados_xml[1])
    
    fill(driver, "input#tbViewDigitalizacaoNf\:itCnpjFornecedor", dados_xml[2]) 
    click(driver, "button#tbViewDigitalizacaoNf\:btnBuscarFornecedor")
    time.sleep(0.5)
    fill(driver, "input#tbViewDigitalizacaoNf\:itNumeroNota", cte)
    fill(driver, "input#tbViewDigitalizacaoNf\:itNumeroSerie", dados_xml[3])
    fill(driver, "input#tbViewDigitalizacaoNf\:calDataEmissao_input", dados_xml[4]+Keys.TAB)
    time.sleep(0.5)

    #Select "Serviço/Produto"
    click(driver, "label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
    time.sleep(0.5)
    while True:
        try:
            for num in range(5):
                servico = driver.find_element(by = By.CSS_SELECTOR, value = "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)).text
                if "frete" in servico.lower():
                    click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                    exit_loop = True
                    break
                elif "não cadastrado" in servico.lower():
                    click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                    exit_loop = True
                    break
            if exit_loop == True:
                break
        except:
            pass

    click(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao")
    fill(driver, "textarea#tbViewDigitalizacaoNf\:itaDescricao", "Frete"+Keys.TAB)

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