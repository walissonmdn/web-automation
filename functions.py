import time
from selenium.webdriver.common.by import By
from xml.dom import minidom
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException

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
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:
            pass
        except ElementClickInterceptedException:
            pass

def fill(driver, css_selector, text): # Fill in a field or upload a file.
    while True:
        try:
            driver.find_element(by = By.CSS_SELECTOR, value = css_selector).send_keys(text)
            break
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:
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
            amount_elements = driver.find_elements(by = By.CSS_SELECTOR, value = 'button#j_idt781')
            amount_elements[-1].click() # Click on the list item of amount_elements list, which is the "Sim" button.
            break
        except:
            pass
           
def dados_xml(cte_path, cte): # Read xml.
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

    return chave