#Legenda:
#cb: combobox
#gb: groupbox
#lb: label
#le: lineedit
#pb: pushbutton
#rb: radiobutton

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from functions import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

class login(QMainWindow): # Tela de Login
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("login_window.ui", self)
        self.show()
        self.pbLogin.clicked.connect(self.check)
    
    def check(self):
        # Validação
        if self.leLogin.text() == "":
            QMessageBox.about(self, "Alerta", "Digite o usuário", )
        
        elif self.leSenha.text() == "":
            QMessageBox.about(self, "Alerta", "Digite a senha", )
        # Passa para a próxima tela
        else:
            self.close()
            self.windows_main = main_window(self.leLogin.text(), self.leSenha.text())
### Fim da classe

class main_window(QMainWindow):   # Tela para inserir linhas e localização
    def __init__(self, usuario, senha):
        super(main_window, self).__init__()
        uic.loadUi("main_window.ui", self)
        self.usuario = usuario
        self.senha = senha
        self.inserir_primeiro_cte = False
        self.config()
        self.show()
        self.cbFormadePagamento.currentTextChanged.connect(self.forma_pagamento_changed) # Chama função quando combobox for alterado
        self.rbSim.toggled.connect(self.rbSim_toggled) # Primeira nota já foi inserida, logo não vai ter boleto
        self.rbNao.toggled.connect(self.rbNao_toggled)
        self.pbProcurarFatura.clicked.connect(self.encontrar_fatura)
        self.pbLocalizacaoCte.clicked.connect(self.encontrar_pasta_cte)
        self.pbLimpar.clicked.connect(self.limpar)
        self.pbIniciar.clicked.connect(self.iniciar)

    # Configuração de elementos da tela
    def config(self):
        self.rbInvisible.setVisible(False) # Botão invisível para forçar os outros a serem desmarcados em situações específicas
        self.rbInvisible_2.setVisible(False) # Botão invisível para forçar os outros a serem desmarcados em situações específicas
        self.leFatura.setReadOnly(True)
        self.leLocalizacaoCte.setReadOnly(True)

    # Quando o combobox da forma de pagamento for alterado
    def forma_pagamento_changed(self):
        if self.cbFormadePagamento.currentText() == "Boleto Agrupado":
            self.gbPrimeiraNota.setEnabled(True) 
            self.lbPrimeiraNota.setEnabled(True)
            self.rbSim.setEnabled(True) 
            self.rbNao.setEnabled(True)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.leFatura.setText("")

        elif self.cbFormadePagamento.currentText() == "Boleto em Anexo":
            self.rbInvisible.setChecked(True)
            self.gbPrimeiraNota.setEnabled(False) 
            self.lbPrimeiraNota.setEnabled(False)
            self.rbSim.setEnabled(False) 
            self.rbNao.setEnabled(False)
            self.pbProcurarFatura.setEnabled(True)
            self.leFatura.setEnabled(True)

        else:
            self.rbInvisible.setChecked(True)
            self.gbPrimeiraNota.setEnabled(False) 
            self.lbPrimeiraNota.setEnabled(False)
            self.rbSim.setEnabled(False) 
            self.rbNao.setEnabled(False)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.leFatura.setText("")

    # Quando o botão "Sim" for marcado ou desmarcado
    def rbSim_toggled(self):
        if self.rbSim.isChecked() == True:
            self.lbPrimeiroCte.setEnabled(True)
            self.lePrimeiroCte.setEnabled(True)
            self.inserir_primeiro_cte = False
        else:
            self.lePrimeiroCte.setEnabled(False)
            self.lePrimeiroCte.setEnabled(False)
            self.inserir_primeiro_cte = True
            self.lePrimeiroCte.setText("")

    # Quando botão "Não" for marcado ou desmarcado
    def rbNao_toggled(self):
        if self.rbNao.isChecked() == True:
            self.gbFatura.setEnabled(True)
            self.leFatura.setEnabled(True)
            self.pbProcurarFatura.setEnabled(True)
        else:
            self.gbFatura.setEnabled(False)
            self.leFatura.setEnabled(False)
            self.pbProcurarFatura.setEnabled(False)
            self.leFatura.setText("")    

    # Quando botão para procurar fatura for clicado
    def encontrar_fatura(self): 
        path = QFileDialog.getOpenFileName()
        path = self.leFatura.setText(path[0])        

    # Quando botão para procurar localização dos documentos de CT-e for clicado
    def encontrar_pasta_cte(self):
        path = QFileDialog.getExistingDirectory()
        path = self.leLocalizacaoCte.setText(path)

    # Quando tudo estiver certo, os dados serão especificados e salvos em variáveis
    def salvar_dados(self):
        if self.rbCitroen.isChecked():
            self.unidade = "11.458.618/0001-16"
        elif self.rbJeep.isChecked():
            self.unidade = "21.214.513/0001-75"
        elif self.rbVolkswagen.isChecked():
            self.unidade = "03.267.961/0001-55"
        elif self.rbParque.isChecked():
            self.unidade = "03.267.961/0004-06"
        
        self.data_vencimento = self.leDatadeVencimento.text()
        self.forma_pagamento = self.cbFormadePagamento.currentText()
        if self.forma_pagamento == "Boleto Agrupado":
            if self.rbSim.isChecked():
                self.inserir_primeiro_cte = False
            elif self.rbNao.isChecked:
                self.inserir_primeiro_cte = True
        else:
            pass
        
        self.fatura_path = self.leFatura
        self.cte_lista = (self.pteCte.toPlainText()).split()
    
    def limpar(self):
        self.rbInvisible_2.setChecked(True)
        self.rbInvisible.setChecked(True)
        self.cbFormadePagamento.setCurrentText("")
        self.lePrimeiroCte.setText("")
        self.leDatadeVencimento.setText("")
        self.leFatura.setText("")
        self.leLocalizacaoCte.setText("")
        self.pteCte.setPlainText("")

    def iniciar(self):
        # Validação
        if self.rbCitroen.isChecked() == False and self.rbJeep.isChecked() == False and self.rbVolkswagen.isChecked() == False and self.rbParque.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a unidade.")
        elif self.cbFormadePagamento.currentText() == "":
            QMessageBox.about(self, "Alerta", "Selecione a forma de pagamento.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == False and self.rbNao.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Selecione a opção relacionada a inserção da primeira nota.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == True and  self.lePrimeiroCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira o número do primeiro CT-e.")
        elif self.leDatadeVencimento.text() == "//":
            QMessageBox.about(self, "Alerta", "Digite a data de vencimento.")
        elif self.cbFormadePagamento.currentText() == "Boleto Agrupado" and self.rbSim.isChecked() == True and  self.leLocalizacaoCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")                   
        elif self.leFatura.text() == "" and self.rbSim.isChecked() == False:
            QMessageBox.about(self, "Alerta", "Insira a Fatura.")
        elif self.leLocalizacaoCte.text() == "":
            QMessageBox.about(self, "Alerta", "Insira a localização dos documentos de CT-e.")
        elif self.pteCte.toPlainText() == "":
            QMessageBox.about(self, "Alerta", "Digite o(s) número(s) do(s) documento(s) de CT-e.")
        # Execução de fato
        else:
            self.salvar_dados()
            self.main = main(self.usuario, self.senha, self.unidade, self.cbFormadePagamento.currentText(), self.inserir_primeiro_cte, self.lePrimeiroCte.text(), self.leDatadeVencimento.text(), self.leFatura.text(), self.leLocalizacaoCte.text(), self.cte_lista)


class main(QMainWindow): # Executa o programa de verificação.
    def __init__(self, usuario, senha, unidade, forma_pagamento, inserir_primeiro_cte, primeiro_cte, data_vencimento, fatura_path, cte_path, cte_lista):
        self.usuario = usuario
        self.senha = senha
        self.unidade = unidade
        self.forma_pagamento = forma_pagamento
        self.inserir_primeiro_cte = inserir_primeiro_cte
        self.data_vencimento = data_vencimento
        self.fatura_path = fatura_path
        self.cte_path = cte_path
        self.cte_lista = cte_lista

        # Caso primero CT-e já tiver sido inserido, especificar número. Do contrário, programa considerará o número do primeiro que será lançado.
        if inserir_primeiro_cte == True:
            self.primeiro_cte = self.cte_lista[0]
        else:
            self.primeiro_cte = primeiro_cte

        # Quantidade de abas que serão abertas.
        if len(self.cte_lista) < 5:
            self.amount_windows = len(self.cte_lista)
        else:
            self.amount_windows = 5 # Caso um boleto agrupado tenha mais de 5 documentos de CT-e, apenas 5 abas serão abertas.
        
        # Executa o programa de lançamento automático.
        execution = self.run()
        if execution == "cte number is wrong": # Parar o programa caso o arquivo de CT-e esteja com o número diferente do xml.
            msg = QMessageBox()
            msg.setWindowTitle("Alerta")
            msg.setText("Número de CT-e do XML está diferente do número do arquivo.") # Será informado na tela do usuário.
            msg.exec_()
        
    def run(self):
        # Inicialização
        driver = webdriver.Edge()
        initialize(driver, self.amount_windows, self.usuario, self.senha)

        # Inicialização de variáveis.
        window_selected = -1 # Haverá incrementação já no primeiro loop
        repeticao_pagina = 1 # Variável necessária, pois botão de confirmação tem o index mudado a cada lançamento na mesma janela
        
        last_cte = self.cte_lista[len(self.cte_lista)-1]

        # Executa laço até que todos os documentos de CT-e tenham sido inseridos.
        for cte in self.cte_lista:

            # Seleciona a janela.
            if window_selected == self.amount_windows - 1:
                window_selected = 0
                repeticao_pagina+=1 # Index inicial do botão é igual a 1
            else:
                window_selected+=1
            
            # Busca chave de acesso no xml do CT-e.
            chave = dados_xml(self.cte_path, cte)
            if chave == False: # Função de cima retorna False caso núm de CT-e no xml esteja diferente do arquivo salvo.
                return "cte number is wrong"

            # Seleciona janela a ser feita a digitalização.
            driver.switch_to.window(driver.window_handles[window_selected])

            #Insere unidade e chave de acesso para digitalização automática.
            click(driver, '//*[@id="btnCriarPedido"]/span[2]')        
            click(driver, '//*[@id="opcoesDigitalizacao"]/tbody/tr/td[4]/div/div[2]/span')
            fill(driver, '//*[@id="itUnidadeCteDigitalizacao_input"]', self.unidade)
            click(driver, '//*[@id="itUnidadeCteDigitalizacao_panel"]/table/tbody/tr')
            time.sleep(0.5)
            fill(driver, '//*[@id="itChaveCteDigitalizacao"]', chave)
            click(driver, '//*[@id="btnEnviarCaptchaCteInformar"]/span[2]')

            # Verifica se unidade já está preenchida e se está correta.
            click(driver, '//*[@id="tbViewDigitalizacaoNf:unidadeOrganizacional_input"]')
            string_unidade = driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:unidadeOrganizacional_input"]').get_attribute("value")
            if self.unidade in string_unidade:
                pass
            else:
                driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:unidadeOrganizacional_input"]').clear() # Apaga valor que foi inserido automaticamente.
                fill(driver, '//*[@id="tbViewDigitalizacaoNf:unidadeOrganizacional_input"]', self.unidade) # Digita CNPJ da unidade.
                click(driver, '//*[@id="tbViewDigitalizacaoNf:unidadeOrganizacional_panel"]/table/tbody/tr') # Seleciona a unidade.
            # Avança.
            click(driver, '//*[@id="tbViewDigitalizacaoNf:btnProximoNota"]/span[2]')
            time.sleep(0.8)

            # Forma de Pagamento.
            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # Boleto agrupado sem nota lançada.
                select = Select(driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:soFormaPagamento_input"]'))
                select.select_by_visible_text('Boleto Agrupado')

            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False: # Boleto agrupado com nota(s) já lançada(s)
                select = Select(driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:soFormaPagamento_input"]'))
                select.select_by_visible_text("Boleto Agrupado")
                click(driver, '//*[@id="tbViewDigitalizacaoNf:sbPrimeiroBoleto"]') # Muda botão de primiera nota para NÃO

            elif self.forma_pagamento == "Boleto em Anexo": # Boleto em anexo
                select = Select(driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:soFormaPagamento_input"]'))
                select.select_by_visible_text("Boleto em anexo")
        
            # Verifica se label "agência" despareceu para dar continuidade.
            while True: 
                try:
                    driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:j_idt402"]/div[1]/div[3]/label[1]')
                except:
                    break    

            # Clica em juros e em CT-e para garantir que campo estará visível.
            click(driver, '//*[@id="tbViewDigitalizacaoNf:accordionAnexos"]/div[5]') 
            click(driver, '//*[@id="tbViewDigitalizacaoNf:accordionAnexos"]/div[1]')

            # Insere pdf do CT-e.
            fill(driver, '//*[@id="tbViewDigitalizacaoNf:accordionAnexos:j_idt465_input"]', self.cte_path + "/" + cte + ".pdf")
            time.sleep(0.5)
            click(driver, '//*[@id="tbViewDigitalizacaoNf:accordionAnexos:j_idt465"]/div[1]/button[1]/span[2]')

            # Data de vencimento.
            while True:
                try:
                    driver.find_element(by = By.XPATH, value = '//*[@id="tbViewDigitalizacaoNf:accordionAnexos:dtAnexoNotaDigitalizacao:0:btnVisualizaAnexoNota"]/span[1]')
                    fill(driver, '//*[@id="tbViewDigitalizacaoNf:calDataVencimento_input"]', self.data_vencimento)
                    click(driver, '//*[@id="tbViewDigitalizacaoNf:accordionAnexos"]/div[3]')
                    break
                except:
                    continue
                
            # Insere boleto ou agrupa nota.
            if self.forma_pagamento == "Boleto em Anexo" or (self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True):
                inserir_boleto(driver, self.fatura_path)
                
            elif self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == False:
                agrupar_nota(driver, self.primeiro_cte, repeticao_pagina)
            
            # Avança.
            click(driver, '//*[@id="tbViewDigitalizacaoNf:btnProximoRateio"]/span[2]')
            time.sleep(0.5)

            # Inserção de rateio.
            click(driver, '//*[@id="tbViewDigitalizacaoNf:btnAdicionarRateio"]/span[2]')# Adicionar.
            # Procura pelo departamento.
            click(driver, '//*[@id="srCentroCustoRateio_label"]') # Expandir lista de departamentos.


            print("Starting now")
            time.sleep(1)
            for num in range(50): #Procura pelo nome Peças.
                centro_rateio = driver.find_element(by = By.XPATH, value = '//*[@id="srCentroCustoRateio_'+str(num)+'"]').text                
                if "Peças" in centro_rateio:
                    #driver.find_element(by = By.XPATH, value = '//*[@id="srCentroCustoRateio_input"]').send_keys(num*Keys.ARROW_DOWN)
                    click(driver, '//*[@id="srCentroCustoRateio_'+str(num)+'"]')
                    break
    
            time.sleep(0.5)

            # Procura pelo usuário aprovador.
            click(driver, '//*[@id="srUsuarioAprovador_label"]') # Expandir lista de usuários
           # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            for num in range(30):   #Procura pelo nome PEDRO FELIPE
                nome_rateio = driver.find_element(by = By.XPATH, value = '//*[@id="srUsuarioAprovador_'+str(num)+'"]').text
                if "PEDRO FELIPE" in nome_rateio:
                    #driver.find_element(by = By.XPATH, value = '//*[@id="srUsuarioAprovador_input"]').send_keys(num*Keys.ARROW_DOWN)
                    click(driver, '//*[@id="srUsuarioAprovador_'+str(num)+'"]')
                    break
            time.sleep(0.5)

            # Insere valor do rateio e salva
            click(driver, '//*[@id="valorRateio_input"]')
            fill(driver, '//*[@id="valorRateio_input"]', '100') # 100% do valor
            click(driver, '//*[@id="btnAdicionarRateio"]/span[2]')
            click(driver, '//*[@id="btnSalvarSolicitacao"]/span[2]')

            # Clica no botão de confirmação para finalizar inserção
            while True:
                try:
                    amount_elements = driver.find_elements(by = By.XPATH, value = '//*[@id="j_idt782"]')
                    amount_elements[-1].click() # Clica no último item da lista amount_elements que é o botão "sim"
                    break
                except:
                    pass

            if self.forma_pagamento == "Boleto Agrupado" and self.inserir_primeiro_cte == True: # Verifica se é a primeira nota e aguarda a inserção ser finalizada.
                self.inserir_primeiro_cte = False
                while True:
                    try:
                        click(driver, '//*[@id="btnCriarPedido"]/span[2]')
                        driver.refresh()
                        break
                    except:
                        pass
            elif cte == last_cte: # Aguardar a finalização da última inserção para só então finalizar o navegador.
                while True:
                    try:
                        click(driver, '//*[@id="btnCriarPedido"]/span[2]')
                        break
                    except:
                        pass

###Fim da classe main    

#Executa a aplicação
app = QApplication(sys.argv)
login_window = login() #Instaciamento da tela de login
app.exec_()


