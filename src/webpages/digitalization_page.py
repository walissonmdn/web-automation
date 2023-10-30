from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time

class DigitalizationPage:
    def __init__(self, driver, legal_person_number) :
        self.driver = driver
        self.legal_person_number = legal_person_number

    def get_digitalization_page(self):
        self.driver.get_page("https://mysaga.gruposaga.com.br/sistema/CSC/digitalizacaoNf/digitalizacaoNF.jsf?faces-redirect=true")
            
    def open_multiple_tabs(self, number_of_tabs):
        # Open 5 tabs at most.
        if number_of_tabs > 1:
            open = 0
            while open < number_of_tabs - 1:
                self.driver.script("window.open('https://mysaga.gruposaga.com.br/sistema/CSC/digitalizacaoNf/digitalizacaoNF.jsf?faces-redirect=true');")
                open+=1
                time.sleep(0.5) 
    
    # Static variable; There'll be an increase in the first loop. 
    tab_index = 0 
    def switch_tabs(self, number_of_tabs):
        # Select window in the browser to digitalize a document.
        self.driver.switch_to_window(DigitalizationPage.tab_index)
        
        if DigitalizationPage.tab_index == number_of_tabs - 1:
            DigitalizationPage.tab_index = 0
        else:
            DigitalizationPage.tab_index += 1

    def find_document_automatically(self, xml_data):
        self.driver.click_loop("button#btnCriarPedido")
        self.driver.click_loop("table#opcoesDigitalizacao > tbody > tr > td:nth-child(4) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default")
        self.driver.fill_loop("input#itUnidadeCteDigitalizacao_input", self.legal_person_number)
        self.driver.click_loop(f"span#itUnidadeCteDigitalizacao_panel > table > tbody > tr[data-item-label*='{self.legal_person_number}']")
        time.sleep(0.5)
        self.driver.fill_loop("input#itChaveCteDigitalizacao", xml_data["access_key"])
        self.driver.click_loop("button#btnEnviarCaptchaCteInformar")
        
    def check_if_document_has_been_found(self):
        while True:
            try:
                self.driver.click(self.driver.find_element("input#tbViewDigitalizacaoNf\:itNumeroNota"))
                document_has_been_found = True
                break
            except:
                try:
                    self.driver.click(self.driver.find_element("button#btnCriarPedido"))
                    document_has_been_found = False
                    break
                except:
                    pass
        return document_has_been_found

    def check_form(self, legal_person_number):
        # Check if "Unidade" has any value and if it's correct.
        string_unidade = self.driver.find_element("input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input")

        if legal_person_number in string_unidade.get_attribute("value"):
            pass
        else:
            self.driver.clear(string_unidade) # Clear the field to fill in again and make sure it'll be correct.
            self.driver.send_keys(string_unidade, legal_person_number)
            self.driver.click_loop("span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+legal_person_number+"']") # Select "unidade".
        
        # Check whether "Serviço/Produto" is already selected and if so, it checks if it's correct.
        while True:
            try:
                string_servico = self.driver.get_text(self.driver.find_element("label#tbViewDigitalizacaoNf\:srServicoFornecedor_label"))
                break
            except StaleElementReferenceException:
                pass

        if "frete" in string_servico.lower():
            pass
        else:
            try:
                for num in range(5):
                    servico = self.driver.get_text(self.driver.find_element("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                    if "frete" in servico.lower():
                        self.driver.click_loop("label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
                        self.driver.click_loop("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                        break
            except:
                self.driver.click_loop("button#tbViewDigitalizacaoNf\:btnBuscarFornecedor")
                self.driver.click_loop("label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
                time.sleep(1)
                try:
                    for num in range(5):
                        servico = self.driver.get_text(self.driver.find_element("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                        if "frete" in servico.lower():
                            self.driver.click_loop("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                            break
                except:
                    for num in range(5):
                        servico = self.driver.get_text(self.driver.find_element("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                        if "não cadastrado" in servico.lower():
                            self.driver.click_loop("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                            break

        self.driver.click_loop("button#tbViewDigitalizacaoNf\:btnProximoNota")
        time.sleep(0.8)

    def fill_in_form(self, document_number, legal_person_number, xml_data):
        self.driver.click_loop("button#j_idt384")
        self.driver.fill_loop('input#tbViewDigitalizacaoNf\:unidadeOrganizacional_input', legal_person_number)
        self.driver.click_loop("span#tbViewDigitalizacaoNf\:unidadeOrganizacional_panel > table > tbody > tr[data-item-label*='"+legal_person_number+"']")
        self.driver.click_loop("table#tbViewDigitalizacaoNf\:srTipoNota > tbody > tr > td:nth-child(1) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default")
        self.driver.fill_loop("input#tbViewDigitalizacaoNf\:itChaveNota", xml_data["access_key"]+Keys.TAB)
        time.sleep(1)

        #Type the value of the "CT-e"
        valor = self.driver.find_element("input#tbViewDigitalizacaoNf\:itValorNota")
        self.driver.clear(valor)
        time.sleep(0.5)
        self.driver.send_keys(valor, xml_data["document_value"])
        time.sleep(0.5)
        self.driver.fill_loop("input#tbViewDigitalizacaoNf\:itCnpjFornecedor", xml_data["legal_person_number"]) 
        self.driver.click_loop("button#tbViewDigitalizacaoNf\:btnBuscarFornecedor")
        time.sleep(0.5)
        self.driver.fill_loop("input#tbViewDigitalizacaoNf\:itNumeroNota", document_number)
        time.sleep(0.5)
        self.driver.fill_loop("input#tbViewDigitalizacaoNf\:itNumeroSerie", xml_data["document_serie_number"])
        time.sleep(0.5)
        self.driver.fill_loop("input#tbViewDigitalizacaoNf\:calDataEmissao_input", xml_data["date_of_issue"]+Keys.TAB)
        time.sleep(0.5)

        self.driver.click_loop("textarea#tbViewDigitalizacaoNf\:itaDescricao")
        self.driver.fill_loop("textarea#tbViewDigitalizacaoNf\:itaDescricao", "Frete"+Keys.TAB)

        #Select "Serviço/Produto"
        exit_loop = False
        while True:
            try:
                self.driver.find_element("li#tbViewDigitalizacaoNf\:srServicoFornecedor_1")
                self.driver.click_loop("label#tbViewDigitalizacaoNf\:srServicoFornecedor_label")
                time.sleep(0.5)
                while True:
                    try:
                        for num in range(5):
                            servico = self.driver.get_text(self.driver.find_element("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num)))
                            if ("frete" in servico.lower()) or ("não cadastrado" in servico.lower()):
                                self.driver.click_loop("li#tbViewDigitalizacaoNf\:srServicoFornecedor_"+str(num))
                                exit_loop = True
                                break
                        print(f"exit_loop: {str(exit_loop)}")
                        if exit_loop == True:
                            while True:
                                try:
                                    self.driver.click(self.driver.find_element("button#tbViewDigitalizacaoNf\:btnProximoNota"))
                                    break
                                except:
                                    try:
                                        valor = self.driver.find_element("input#tbViewDigitalizacaoNf\:itValorNota")
                                        self.driver.clear(valor)
                                        time.sleep(0.5)
                                        self.driver.send_keys(valor, xml_data["document_value"])
                                        time.sleep(0.5)

                                        num_cte = self.driver.find_element("input#tbViewDigitalizacaoNf\:itNumeroNota")
                                        self.driver.clear(num_cte)
                                        time.sleep(0.5)
                                        self.driver.send_keys(num_cte, document_number)
                                        time.sleep(0.5)
                                        self.driver.click_loop("textarea#tbViewDigitalizacaoNf\:itaDescricao")

                                        num_serie = self.driver.find_element("input#tbViewDigitalizacaoNf\:itNumeroSerie")
                                        self.driver.clear(num_serie)
                                        time.sleep(0.5)
                                        self.driver.send_keys(num_serie, xml_data["document_serie_number"])
                                        time.sleep(0.5)
                                        self.driver.click_loop("textarea#tbViewDigitalizacaoNf\:itaDescricao")

                                        data_emissao = self.driver.find_element("input#tbViewDigitalizacaoNf\:calDataEmissao_input")
                                        self.driver.clear(data_emissao)
                                        time.sleep(0.5)
                                        self.driver.send_keys(data_emissao, xml_data["date_of_issue"]+Keys.TAB)
                                        time.sleep(0.5)
                                        self.driver.click_loop("textarea#tbViewDigitalizacaoNf\:itaDescricao")
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
                    self.driver.click(self.driver.find_element("button#tbViewDigitalizacaoNf\:btnProximoNota"))
                    time.sleep(0.8)
                    break
                except:
                    pass

    def select_payment_method(self, payment_method, insert_first_cte):
        while True:
            try:
                payment = self.driver.select(self.driver.find_element("select#tbViewDigitalizacaoNf\:soFormaPagamento_input"))
                break
            except:
                pass
        if payment_method == "Boleto Agrupado" and insert_first_cte == True: # "Boleto agrupado" and no "CT-e" inserted.
            self.driver.select_by_visible_text(payment, "Boleto Agrupado")

        elif payment_method == "Boleto Agrupado" and insert_first_cte == False: # "Boleto agrupado" and there's already "CT-e" inserted.
            self.driver.select_by_visible_text(payment, "Boleto Agrupado")
            self.driver.click_loop("div#tbViewDigitalizacaoNf\:sbPrimeiroBoleto") # Change "Primeira nota?" button to "Não"

        elif payment_method == "Boleto em Anexo": # "Boleto em anexo"
            self.driver.select_by_visible_text(payment, "Boleto em anexo")

    def upload_document(self, document_path, document_number):
        self.driver.fill_loop("div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > span > input[type=file]", f"{document_path}/{document_number}.pdf")
        time.sleep(0.5)
        self.driver.click_loop( "div#tbViewDigitalizacaoNf\:accordionAnexos\:pnAnexosNota_content > div.ui-fileupload.ui-widget.ui-fileupload-responsive > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload")

    def fill_in_due_date(self, due_date):
        # "Data de vencimento".
        while True:
            try:
                self.driver.find_element("button#tbViewDigitalizacaoNf\:accordionAnexos\:dtAnexoNotaDigitalizacao\:0\:btnVisualizaAnexoNota")
                self.driver.fill_loop("input#tbViewDigitalizacaoNf\:calDataVencimento_input", due_date)
                self.driver.click_loop("div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)")
                break
            except:
                continue
    
    def upload_invoice(self, invoice_path):
        self.driver.click_loop('div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
        self.driver.click_loop('button#tbViewDigitalizacaoNf\:accordionAnexos\:dtBoletoDigitalizacao\:0\:btnAdicionaBoleto')
        self.driver.fill_loop('input#fileUploadBoleto_input', invoice_path)
        self.driver.click_loop('div#fileUploadBoleto > div.ui-fileupload-buttonbar.ui-widget-header.ui-corner-top > button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-icon-left.ui-fileupload-upload')

    def relate_documents(self, first_document_number):
        self.driver.click_loop('div#tbViewDigitalizacaoNf\:accordionAnexos > div:nth-child(3)')
        time.sleep(0.5)
        while True:
            try:
                first_document_field = self.driver.find_element("input#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:j_idt676\:filter")
                self.driver.send_keys(first_document_field, first_document_number)
                break
            except:
                pass

        time.sleep(0.5)
                                                                  
        while True:
            try:
                self.driver.click(self.driver.find_element("#tbViewDigitalizacaoNf\:accordionAnexos\:dtDigitalizacaoNFAgrupado\:0\:j_idt685"))
                print("clicked")
                break
            except:
                pass
        time.sleep(0.5)

        while True:
            try:
                amount_elements = self.driver.find_elements("button#j_idt448") 
                self.driver.click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                break
            except:
                pass

    def insert_payer(self):
        # Insert "rateio".
        self.driver.click_loop("button#tbViewDigitalizacaoNf\:btnAdicionarRateio")# "Adicionar" button.

        # Search for the departament.
        self.driver.click_loop("label#srCentroCustoRateio_label") # Expand department list.
        time.sleep(1)
        for num in range(50): # Search for "Peças".
            centro_rateio = self.driver.get_text(self.driver.find_element(f"li#srCentroCustoRateio_{str(num)}"))
            if "Peças" in centro_rateio:
                self.driver.click_loop(f"li#srCentroCustoRateio_{str(num)}")
                break

        time.sleep(0.5)

        # Search for the user. 
        self.driver.click_loop("label#srUsuarioAprovador_label") # Expand user list.
        time.sleep(1)
        for num in range(30):   # Search for Pedro #srUsuarioAprovador_1
            nome_rateio = self.driver.get_text(self.driver.find_element(f"li#srUsuarioAprovador_{str(num)}"))
            if "PEDRO FELIPE FERREIRA LEITE" in nome_rateio:
                self.driver.click_loop(f"li#srUsuarioAprovador_{str(num)}")
                break
        time.sleep(0.5)

        # Insert value of "rateio".
        self.driver.click_loop('input#valorRateio_input')
        self.driver.fill_loop('input#valorRateio_input', '100') # 100% of the value.
        self.driver.click_loop('button#btnAdicionarRateio')

    def save(self):    
        self.driver.click_loop('button#btnSalvarSolicitacao')

        # Confirm and finish.
        while True:
            try:
                amount_elements = self.driver.find_elements("button#j_idt789")
                self.driver.click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                break
            except:
                try:
                    amount_elements = self.driver.find_elements("button#j_idt448")
                    self.driver.click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                    break
                except:
                    try:
                        amount_elements = self.driver.find_elements("button#j_idt790")
                        self.driver.click(amount_elements[-1]) # Click on the last element of the list "amount_elements", which is the "Sim" button.
                        break
                    except:
                        pass

    def await_unitl_first_digitalization_finishes(self):
        while True:
            try:
                self.driver.click_loop("#btnCriarPedido")
                self.driver.refresh()
                break
            except:
                pass

    def await_until_last_digitalization_finishes(self):
        while True:
            try:
                self.driver.click_loop("#btnCriarPedido")
                break
            except:
                pass