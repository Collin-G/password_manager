import sys
import json
from PySide2 import QtWidgets, QtGui, QtCore
from keygen import KeyGen
from encyrption import Encryption

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = None
        self.n = None
        self.e = None

        self.layout = QtWidgets.QVBoxLayout(self)
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

        self.layout.addWidget(self.select_combo)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.site_edit)
        self.layout.addWidget(self.user_edit)
        self.layout.addWidget(self.pass_edit)

        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_creds)
        self.load_button.clicked.connect(self.load_creds)
        self.delete_button.clicked.connect(self.delete_creds)

        self.get_options()
    
    def delete_creds(self):
        row = self.select_combo.currentIndex()
        site = self.select_combo.itemText(row)
        self.select_combo.removeItem(row)
        with open("creds.json","r") as f:
            creds = json.load(f)
        index = [cred.get("site") for cred in  creds].index(site)
        creds.pop(index)

        with open("creds.json", "w") as f:
            json.dump(creds,f)
        
    
    def get_options(self):
        with open("creds.json","r") as f:
            creds = json.load(f)
        self.select_combo.addItems(cred.get("site") for cred in creds)
    
    def load_creds(self):
        self.verify_keygen()
        e = Encryption(self.d,self.n,self.e)
        site = self.select_combo.itemText(self.select_combo.currentIndex())
        with open("creds.json","r") as f:
            creds = json.load(f)
            for cred in creds:
                if cred.get("site") == site:
                    passw = cred.get("password")
                    user = cred.get("username")
                    break
        self.site_edit.setText(site)
        self.user_edit.setText(e.decrypt(user))
        self.pass_edit.setText(e.decrypt(passw))
        

    def save_creds(self):
        items = [self.select_combo.itemText(i) for i in range(self.select_combo.count())]
        if self.site_edit.text() in items:
            return
        self.verify_keygen()
        if not (self.site_edit.text() and self.user_edit.text() and self.pass_edit.text()):
            return
        e = Encryption(self.d,self.n,self.e)
        user = e.encrypt(self.user_edit.text())
        passw = e.encrypt(self.pass_edit.text())
        with open("creds.json","r") as f:
            creds = json.load(f)
            creds.append({"site" : self.site_edit.text(), "username" : user, "password": passw})
        
        with open("creds.json", "w") as f:
            json.dump(creds,f)
        
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
