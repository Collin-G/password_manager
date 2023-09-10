import sys
import json
import pandas as pd
from ast import literal_eval
from PySide2 import QtWidgets, QtGui, QtCore
from keygen import KeyGen
from encyrption import Encryption

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = None
        self.n = None
        self.e = None
        self.resize(300,200)
        self.layout = QtWidgets.QFormLayout(self)
        self.setLayout(self.layout)
        self.select_combo = QtWidgets.QComboBox()
        self.site_edit = QtWidgets.QLineEdit()
        self.site_edit.setPlaceholderText("Site")
        self.user_edit = QtWidgets.QLineEdit()
        self.user_edit.setPlaceholderText("User Name")
        self.pass_edit = QtWidgets.QLineEdit()
        self.pass_edit.setPlaceholderText("Password")
        self.save_button = QtWidgets.QPushButton("Save")
        self.load_button = QtWidgets.QPushButton("Load")
        self.delete_button = QtWidgets.QPushButton("Delete")
        
        self.h_layout = QtWidgets.QHBoxLayout()
        self.layout.addRow("Load Creds: ", self.select_combo)
        self.layout.addRow(self.h_layout)
        self.h_layout.addWidget(self.load_button)
        self.h_layout.addWidget(self.delete_button)
        self.layout.addRow("Site: ",self.site_edit)
        self.layout.addRow("Username: ",self.user_edit)
        self.layout.addRow("Password: ", self.pass_edit)

        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_creds)
        self.load_button.clicked.connect(self.load_creds)
        self.delete_button.clicked.connect(self.delete_creds)

        self.get_options()
    
    def delete_creds(self):
        
        row = self.select_combo.currentIndex()
        site = self.select_combo.itemText(row)
        if not site:
            return
        self.select_combo.removeItem(row)
        df = pd.read_csv("data.csv", index_col=0)
        df = df.drop(site)
        df.to_csv("data.csv")  
    
    def get_options(self):
        df = pd.read_csv("data.csv", index_col=0)
        items = df["site"].values.tolist()
        self.select_combo.addItems(items)
      
    def load_creds(self):
        self.verify_keygen()
        e = Encryption(self.d,self.n,self.e)
        site = self.select_combo.itemText(self.select_combo.currentIndex())
        if not site:
            return
        df = pd.read_csv("data.csv", index_col=0)
        user = df.at[site, "username"]
        passw = df.at[site, "password"]
       
        self.site_edit.setText(site)
        self.user_edit.setText(e.decrypt(literal_eval(user)))
        self.pass_edit.setText(e.decrypt(literal_eval(passw)))
        

    def save_creds(self):
        items = [self.select_combo.itemText(i) for i in range(self.select_combo.count())]
        self.verify_keygen()
        if not (self.site_edit.text() and self.user_edit.text() and self.pass_edit.text()):
            return
        e = Encryption(self.d,self.n,self.e)
        user = e.encrypt(self.user_edit.text())
        passw = e.encrypt(self.pass_edit.text())

        df = pd.read_csv("data.csv", index_col=0)
        df.loc[self.site_edit.text()]=[self.site_edit.text(),user, passw]
        df.to_csv("data.csv")
        if self.site_edit.text() not in items:
            self.select_combo.addItem(self.site_edit.text())


    def verify_keygen(self):
        with open("public.json", "r") as f:
            pub = json.load(f)
        with open("private.json", "r") as f:
            priv = json.load(f)

        if pub.get("e") and pub.get("n") and priv.get("d"):
            self.e = pub.get("e")
            self.n = pub.get("n")
            self.d = priv.get("d")
        else:
            kg = KeyGen()
            self.e = kg.e
            self.d = kg.d
            self.n = kg.n
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
