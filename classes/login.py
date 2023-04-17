# Contractions:
# cb: combobox
# gb: groupbox
# lb: label
# le: lineedit
# pb: pushbutton
# rb: radiobutton

from classes.form import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class login(QMainWindow): # Login window.
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("ui\\login_window.ui", self)
        self.show()
        self.pbLogin.clicked.connect(self.check)
    
    def check(self):
        # Validation.
        if self.leUser.text() == "":
            QMessageBox.about(self, "Atenção!", "Digite o usuário.", )
        
        elif self.lePassword.text() == "":
            QMessageBox.about(self, "Atenção!", "Digite a senha.", )
        
        else: # Make an instance of the next window.
            self.close()
            self.windows_main = form(self.leUser.text(), self.lePassword.text())
### End of class "login".