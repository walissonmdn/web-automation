from xml.dom import minidom

class XMLDataExtractor:
    def __init__(self, document_number, document_path):
        self.document_number = document_number
        self.document_path = document_path

    def open_xml_file(self):
        self.xml_file = open(f"{self.document_path}/{self.document_number}.xml")
        
    def extract_data(self):
        self.open_xml_file()
        xml_data = minidom.parse(self.xml_file)
        
        document_number_element = xml_data.getElementsByTagName("nCT")
        document_number = document_number_element[0].firstChild.data

        access_key_element = xml_data.getElementsByTagName("chCTe")
        access_key = access_key_element[0].firstChild.data

        document_value_element = xml_data.getElementsByTagName("vRec")
        document_value = document_value_element[0].firstChild.data

        legal_person_number_element = xml_data.getElementsByTagName("CNPJ")
        legal_person_number = legal_person_number_element[0].firstChild.data

        document_serie_number_element = xml_data.getElementsByTagName("serie")
        document_serie_number = document_serie_number_element[0].firstChild.data

        date_of_issue_element = xml_data.getElementsByTagName("dhEmi")
        date_of_issue = date_of_issue_element[0].firstChild.data
        date_of_issue_formatted = f"{date_of_issue[8]}{date_of_issue[9]}/{date_of_issue[5]}{date_of_issue[6]}/{date_of_issue[0]}{date_of_issue[1]}{date_of_issue[2]}{date_of_issue[3]}"

        return {"document_number": document_number, "access_key": access_key,
            "document_value": document_value,
            "legal_person_number": legal_person_number, 
            "document_serie_number": document_serie_number, 
            "date_of_issue": date_of_issue_formatted
        }
    

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