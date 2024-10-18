#-------------------- KÜTÜPHANE --------------------
#---------------------------------------------------
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from voiceCommandDatabase import *

#---------------- UYGULAMA OLUŞTURMA ---------------
#---------------------------------------------------

# Öncelikle Uygulama Nesnesi Oluşturuyoruz
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

#--------------- VERİTABANI OLUŞTURMA --------------
#---------------------------------------------------

import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblSpor=("CREATE TABLE IF NOT EXISTS voice(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
                 Language TEXT NOT NULL,                       \
                 Gender TEXT NOT NULL,                         \
                 Name TEXT NOT NULL,                      \
                 Commend TEXT NOT NULL,                          \
                 Url TEXT NOT NULL UNIQUE,                             \
                 Status BOOLEAN NOT NULL )")
curs.execute(sorguCreTblSpor)# Bu yazdığımız sorguyu execute eder
conn.commit()

sys.exit(Uygulama.exec_())