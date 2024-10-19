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
queryCreTblVoice = (
    "CREATE TABLE IF NOT EXISTS voice(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
                 Language TEXT NOT NULL,                       \
                 Gender TEXT NOT NULL,                         \
                 Name TEXT NOT NULL,                      \
                 Commend TEXT NOT NULL,                          \
                 Url TEXT NOT NULL UNIQUE,                             \
                 Status BOOLEAN NOT NULL )"
)
curs.execute(queryCreTblVoice)
conn.commit()
#--------------- VERİTABANINDAN VERİ ÇEKME --------------
def LISTALLDATA():
    scrollAreaWidgetContents_2 = ui.scrollAreaWidgetContents_2
    if scrollAreaWidgetContents_2.layout() is None:
        verticalLayout = QVBoxLayout(scrollAreaWidgetContents_2)
        scrollAreaWidgetContents_2.setLayout(verticalLayout)
        print("Yeni layout oluşturuldu.")
    else:
        verticalLayout = scrollAreaWidgetContents_2.layout()
        print("Mevcut layout bulundu.")

    for i in reversed(range(verticalLayout.count())):
        widget_to_remove = verticalLayout.itemAt(i).widget()
        if widget_to_remove is not None:
            widget_to_remove.deleteLater()

    curs.execute("SELECT * FROM voice")
    # Verileri kullanarak CustomWidget oluştur
    for satirVeri in curs:
        # satirVeri'yi dictionary formatında alıyorsanız, ona göre verileri ayarlayın
        data = {
            "Language": satirVeri[1],
            "Gender": satirVeri[2],
            "Name": satirVeri[3],
            "Commend": satirVeri[4],
            "Progress": 0
        }

        custom_widget = CustomWidget(data["Language"], data["Gender"], data["Name"], data["Commend"],data["Progress"])
        verticalLayout.addWidget(custom_widget)
        print(f"Widget eklendi: {data['Name']}")
    curs.execute("SELECT COUNT(*) FROM voice")
    print("Sorgu")
    numberVoice = curs.fetchone()
    ui.labelShowedDataNumber.setText(str(numberVoice[0]))


def FILTERDATA():
    # Dil kontrolleri
    english_selected = ui.radioButtonFilterLanguageEnglish.isChecked()
    turkish_selected = ui.radioButtonFilterLanguageTurkish.isChecked()
    print("OKEY")
    # Cinsiyet kontrolleri
    male_selected = ui.radioButtonFilterGenderMale.isChecked()
    female_selected = ui.radioButtonFilterGenderFemale.isChecked()
    print("OKEY")
    # Dil kontrolü
    if not (turkish_selected or english_selected):
        QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen en az bir dil seçin.")
        return  # Fonksiyonu sonlandır
    print("OKEY")
    # Cinsiyet kontrolü
    if not (male_selected or female_selected):
        QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen en az bir cinsiyet seçin.")
        return  # Fonksiyonu sonlandır
    print("OKEY")
    # Seçilen dillerin listesini oluştur
    languages = []
    if turkish_selected:
        languages.append("tr")
    if english_selected:
        languages.append("en")
    print("OKEY")
    # Seçilen cinsiyetlerin listesini oluştur
    genders = []
    if male_selected:
        genders.append("male")
    if female_selected:
        genders.append("female")
    print("OKEY")
    name_selected = ui.comboBoxFilterName.currentText()
    print(name_selected)
    commend_selected = ui.comboBoxFilterCommend.currentText()
    print(commend_selected)
    # Sorguyu oluştur
    query = "SELECT * FROM voice WHERE (Language IN ({}) AND Gender IN ({})".format(
        ', '.join('?' * len(languages)),
        ', '.join('?' * len(genders))
    )
    print("OKEY")
    # Name koşulunu ekle


    if name_selected != "All":
        query += " AND Name=?)"
        params = languages + genders + [name_selected, commend_selected]
    else:
        query += ")"
        params = languages + genders

    print("OKEY")
    # Commend koşulunu kontrol et
    if commend_selected != "All":
        query += " AND Commend=?)"
        params = languages + genders + [name_selected, commend_selected]
    else:
        query += ")"
        params = languages + genders + [name_selected]

    # Filtreleme sorgusu
    curs.execute(query, params)
    print("OKEY")
    # Sonuçları işleme
    results = curs.fetchall()

    scrollAreaWidgetContents_2 = ui.scrollAreaWidgetContents_2

    if scrollAreaWidgetContents_2.layout() is None:
        verticalLayout = QVBoxLayout(scrollAreaWidgetContents_2)
        scrollAreaWidgetContents_2.setLayout(verticalLayout)
        print("Yeni layout oluşturuldu.")
    else:
        verticalLayout = scrollAreaWidgetContents_2.layout()
        print("Mevcut layout bulundu.")

    # Mevcut widget'ları temizle
    for i in reversed(range(verticalLayout.count())):
        widget_to_remove = verticalLayout.itemAt(i).widget()
        if widget_to_remove is not None:
            widget_to_remove.deleteLater()

    # Sonuçları widget'lara ekle
    for satirVeri in results:
        data = {
            "Language": satirVeri[1],
            "Gender": satirVeri[2],
            "Name": satirVeri[3],
            "Commend": satirVeri[4],
            "Progress": 0  # Progress değerini uygun bir kaynaktan almak gerekebilir
        }

        custom_widget = CustomWidget(data["Language"], data["Gender"], data["Name"], data["Commend"], data["Progress"])
        verticalLayout.addWidget(custom_widget)
        print(f"Widget eklendi: {data['Name']}")
        print("OKEY")

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
ui.pushButtonButtonsShowAllData.clicked.connect(LISTALLDATA)
ui.pushButtonButtonsFilterData.clicked.connect(FILTERDATA)

sys.exit(Uygulama.exec_())
