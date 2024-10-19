#-------------------- KÜTÜPHANE --------------------
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from voiceCommandDatabase import *
from PyQt5 import uic
import sqlite3

#---------------- ÖZEL WIDGET TANIMI ---------------
class CustomWidget(QtWidgets.QWidget):
    def __init__(self, name, language, gender, commend, progress):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)

        # Border'ı ayarla
        self.setStyleSheet(
            "border-style: solid;"
            "border-width: 3px;"
            "border-color: #4d4018;"
        )

        # Play Butonu
        self.pushButtonCardExamplePlay = QPushButton('Play')
        self.pushButtonCardExamplePlay.setStyleSheet(
            "QPushButton {"
            "border-style: solid;"
            "border-width: 3px;"
            "background-color: #ff6d49;"
            "border-color: #4d4018;"
            "color: black;"
            "}"
            "QPushButton:hover {"
            "background-color: red;"
            "}"
        )
        layout.addWidget(self.pushButtonCardExamplePlay)

        # Language Label
        self.labelCardExampleLanguage = QLabel(language)
        self.labelCardExampleLanguage.setStyleSheet(
            "background-color: #ff9b0f;"
            "color: black;"
            "border-color: #4d4018;"
        )
        layout.addWidget(self.labelCardExampleLanguage)

        # Gender Label
        self.labelCardExampleGender = QLabel(gender)
        self.labelCardExampleGender.setStyleSheet(
            "background-color: #ff9b0f;"
            "color: black;"
            "border-color: #4d4018;"
        )
        layout.addWidget(self.labelCardExampleGender)

        # Name Label
        self.labelCardExampleName = QLabel(name)
        self.labelCardExampleName.setStyleSheet(
            "background-color: #ff9b0f;"
            "color: black;"
            "border-color: #4d4018;"
        )
        layout.addWidget(self.labelCardExampleName)

        # Voice Command Label
        self.labelCardExampleCommend = QLabel(commend)
        self.labelCardExampleCommend.setStyleSheet(
            "background-color: #ff9b0f;"
            "color: black;"
            "border-color: #4d4018;"
        )
        layout.addWidget(self.labelCardExampleCommend)

        # Progress Bar
        self.progressBarCardExample = QProgressBar()
        self.progressBarCardExample.setStyleSheet(
            "background-color: black;"
            "border-color: #4d4018;"
        )
        self.progressBarCardExample.setValue(progress)
        layout.addWidget(self.progressBarCardExample)

#---------------- UYGULAMA OLUŞTURMA ---------------
Uygulama = QApplication(sys.argv)
penAna = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(penAna)

#--------------- VERİTABANI OLUŞTURMA --------------
global curs
global conn
conn = sqlite3.connect('veritabani.db')
curs = conn.cursor()
sorguCreTblSpor = (
    "CREATE TABLE IF NOT EXISTS voice(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
                 Language TEXT NOT NULL,                       \
                 Gender TEXT NOT NULL,                         \
                 Name TEXT NOT NULL,                      \
                 Commend TEXT NOT NULL,                          \
                 Url TEXT NOT NULL UNIQUE,                             \
                 Status BOOLEAN NOT NULL )"
)
curs.execute(sorguCreTblSpor)
conn.commit()

#--------------- WIDGET EKLEME ----------------------
# scrollAreaWidgetContents_2'yi al
scrollAreaWidgetContents_2 = ui.scrollAreaWidgetContents_2

# Eğer scrollAreaWidgetContents_2 için bir layout yoksa oluştur
if scrollAreaWidgetContents_2.layout() is None:
    verticalLayout = QVBoxLayout(scrollAreaWidgetContents_2)
    scrollAreaWidgetContents_2.setLayout(verticalLayout)
    print("Yeni layout oluşturuldu.")
else:
    verticalLayout = scrollAreaWidgetContents_2.layout()
    print("Mevcut layout bulundu.")

# Mevcut widget'ları temizleme
for i in reversed(range(verticalLayout.count())):
    widget_to_remove = verticalLayout.itemAt(i).widget()
    if widget_to_remove is not None:
        widget_to_remove.deleteLater()

# Yeni widget'ları ekle
widget_data = [
    {"name": "John", "language": "English", "gender": "Male", "commend": "Jump", "progress": 50},
    {"name": "Alice", "language": "French", "gender": "Female", "commend": "Run", "progress": 30},
    {"name": "Bob", "language": "German", "gender": "Male", "commend": "Sit", "progress": 70},
    {"name": "Eve", "language": "Spanish", "gender": "Female", "commend": "Walk", "progress": 80},
    {"name": "Tom", "language": "Turkish", "gender": "Male", "commend": "Stand", "progress": 60},
]

for data in widget_data:
    custom_widget = CustomWidget(data["name"], data["language"], data["gender"], data["commend"], data["progress"])
    verticalLayout.addWidget(custom_widget)
    print(f"Widget eklendi: {data['name']}")

# Uygulamayı başlat
penAna.show()


# Clear butonuna tıklanınca çalışacak fonksiyon
def clear_widgets():
    layout = ui.scrollAreaWidgetContents_2.layout()

    if layout is not None:
        # Layout içerisindeki tüm widget'ları sil
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
        print("Tüm widget'lar silindi.")


# Clear butonunu clicked sinyaline bağla
ui.pushButtonButtonsClearData.clicked.connect(clear_widgets)

sys.exit(Uygulama.exec_())
