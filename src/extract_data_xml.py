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

        return {
            "document_number": document_number, 
            "access_key": access_key,
            "document_value": document_value,
            "legal_person_number": legal_person_number, 
            "document_serie_number": document_serie_number, 
            "date_of_issue": date_of_issue_formatted
        }
    