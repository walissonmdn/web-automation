from src.windows.login_window import *
from PyQt5.QtWidgets import QApplication
import sys

#Execute the software.
app = QApplication(sys.argv)
login_window = Login() # Make an instance from login class.
app.exec_()  
