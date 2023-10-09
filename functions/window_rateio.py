from functions.selenium_functions import *
from functions.general_functions import *
import time

def fill_department(driver, ):
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
