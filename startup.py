from classes.login import *
from functions import *
from PyQt5.QtWidgets import QApplication
import sys

#Execute the software.
app = QApplication(sys.argv)
login_window = login() # Make an instance from login class.
app.exec_()