from functions.selenium_functions import *
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, NoSuchWindowException
from selenium.webdriver.common.by import By
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