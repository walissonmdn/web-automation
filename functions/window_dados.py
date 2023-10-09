from functions.selenium_functions import *
from functions.general_functions import *
import time

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
                        if "frete" in servico.lower():
                            click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                            click(driver, "button#tbViewDigitalizacaoNf\:btnProximoNota")
                            time.sleep(0.8)
                            exit_loop = True
                            break
                        elif "não cadastrado" in servico.lower():
                            click(driver, "li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                            click(driver, "button#tbViewDigitalizacaoNf\:btnProximoNota")
                            time.sleep(0.8)
                            exit_loop = True
                            break
                    if exit_loop == True:
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


def fill_cte_data(driver, cte, cnpj, dados_xml):
    while True:
        try:
            selenium_click(selenium_find_element(driver, "input#tbViewDigitalizacaoNf\:itNumeroNota")) # Verify whether the "CT-e" was imported automatically. 
            digitalizacao_automatica_cte(driver, cnpj)
            break
        except:
            try:
                selenium_click(selenium_find_element(driver, "button#btnCriarPedido"))
                digitalizacao_manual_cte(driver, cte, cnpj, dados_xml)
                break
            except:
                pass