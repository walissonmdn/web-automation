#Caption:
#cb: combobox
#gb: groupbox
#lb: label
#le: lineedit
#pb: pushbutton
#rb: radiobutton

from classes.form import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class login(QMainWindow): # Login Screen
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("ui\\login_window.ui", self)
        self.show()
        self.pbLogin.clicked.connect(self.check)
    
    def check(self):
        # Validation
        if self.leLogin.text() == "":
            QMessageBox.about(self, "Alerta", "Digite o usuário", )
        
        elif self.leSenha.text() == "":
            QMessageBox.about(self, "Alerta", "Digite a senha", )
        # Create an instance of main_windows
        else:
            self.close()
            self.windows_main = form(self.leLogin.text(), self.leSenha.text())
### End of class "login".