"""
Öğrenci Adı Soyadı: Hüseyin Karabulut 
Öğrenci No:2112721044
"""

# İlgili Kütüphaneleri içeri aktaralım
import sys
import numpy as np  # Diziler ve matematik işlemleri için

# Kendi oluşturduğumuz Genetik algoritma modülümüzü içeri aktaralım
import GA

# PyQt5'den gerekli modüller
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListView,
    QMessageBox,
)


class GeneticAlgorithmUI(QWidget):
    def __init__(self):
        super().__init__()
        self.user_inputs = (
            []
        )  # Kullanıcı Giriş alanlarını depolamak için bir liste oluşturduk
        self.initUI()

    def initUI(self):
        # Arayüzün genel görünümü ve stil ayarlarını burada yapılandırıyoruz
        self.setStyleSheet("background-color: #120d23;")
        self.setWindowTitle("Genetik Algoritma")
        self.setGeometry(100, 100, 800, 600)

        # Uygulama ikonunu ayarlama kısmı
        app_icon = QIcon("logo.png")  # İkonumuzun yolunu belirtiyoruz
        self.setWindowIcon(app_icon)

        # Yatayda ana bir layout oluşturuyoruz
        main_layout = QHBoxLayout(self)

        # Fotoğraf bölümünün olduğu kısım
        image_pixmap = QPixmap("ga.png").scaled(
            400, 930
        )  # Fotoğrafı ekleyip genişliğini belirtiyoruz
        image_label = QLabel()
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(
            image_label, 1
        )  # Yatay ana layout'un 1/4'lük kısmına fotoğrafı koyuyoruz

        # Diğer bileşenlerin yerleşimi için layout'lar
        right_vertical_layout = QVBoxLayout()  # Dikey bir layout oluşturuyoruz
        main_layout.addLayout(
            right_vertical_layout, 3
        )  # Yatay ana layout'un 3/4'lük kısmına diğer bileşenleri koyuyoruz

        # ListView bölümünün olduğu kısım
        self.result_list_view = QListView()
        self.result_list_view.setStyleSheet(
            "background-color: white; font-weight: bold;"
        )
        self.result_list_view.setFixedSize(1300, 350)
        right_vertical_layout.addWidget(
            self.result_list_view, 2
        )  # Dikey layout'un 2/5'lik kısmına ListView'ı yerleştiriyoruz

        # Labellar ve text alanlarının olduğu kısım
        user_inputs_labels = [
            "Denklem Girdileri (virgülle ayrılmış): ",
            "Ağırlıkların Sayısı: ",
            "Popülasyon Başına Çözüm Sayısı: ",
            "Alt Sınır: ",
            "Üst Sınır: ",
            "Jenerasyon (Nesil) Sayısı: ",
            "Eşleşme Havuzundaki Birey Sayısı: ",
        ]
        for label_text in user_inputs_labels:
            input_horizontal_layout = (
                QHBoxLayout()
            )  # Label ve metin kutusunu yatay olarak sıralamak için QHBoxLayout kullandık

            label = QLabel(label_text)
            label.setStyleSheet("color: white; font-weight: bold;")
            label_font = QFont("Montserrat", 8)  # Özel bir font kullandık
            label.setFont(label_font)  # Buton metin fontunu ayarladık
            input_horizontal_layout.addWidget(label)  # Label'ları QHBoxLayout'a ekledik

            input_field = QLineEdit()
            input_field.setFixedWidth(150)  # Metin alanının genişliği
            input_field.setStyleSheet("background-color: white; color: black;")
            input_font = QFont("Montserrat", 8)  # Özel bir font oluşturalım
            input_field.setFont(input_font)  # Buton metin fontunu ayarlayalım
            self.user_inputs.append(
                input_field
            )  # Oluşturulan input alanlarını user_inputs adlı listeye ekleyelim
            input_horizontal_layout.addWidget(
                input_field
            )  # Textbox'ları (input alanlarını) QHBoxLayout'a ekledim

            # Metin kutusu için bir miktar boşluk ekledim
            input_horizontal_layout.addSpacing(1000)

            right_vertical_layout.addLayout(
                input_horizontal_layout
            )  # QHBoxLayout'u ana dikey layout içine ekliyoruz. Burası da geri kalan 3/5'lik kısmı kaplıyor.

        # 'OLUŞTUR' butonu için gerekli ayarlamaları yapıyoruz
        self.generate_button = QPushButton("OLUŞTUR")
        self.generate_button.setStyleSheet(
            "background-color: #1069d8; color: white; font-weight: bold;"
        )
        generate_font = QFont("Verdana", 10)  # Özel bir font oluşturalım
        self.generate_button.setFont(generate_font)  # Buton metin fontunu ayarlayalım
        self.generate_button.clicked.connect(self.runGeneticAlgorithm)
        right_vertical_layout.addWidget(self.generate_button)
        self.generate_button.setFixedSize(900, 35)  # Butonun genişlik ve yüksekliği

        # 'TEMİZLE' butonu için gerekli ayarlamaları yapıyoruz
        clear_button = QPushButton("TEMİZLE")
        clear_button.setStyleSheet(
            "background-color: white; color: #1069d8; font-weight: bold;"
        )
        clear_font = QFont("Montserrat", 10)  # Özel bir font oluşturalım
        clear_button.setFont(clear_font)  # Buton metin fontunu ayarlayalım
        clear_button.clicked.connect(self.clearListView)
        right_vertical_layout.addWidget(clear_button)
        clear_button.setFixedSize(900, 35)  # Butonun genişlik ve yüksekliği

    def runGeneticAlgorithm(self):
        try:
            # Kullanıcı girişlerini alalım
            equation_user_inputs = [
                float(x.strip()) for x in self.user_inputs[0].text().split(",")
            ]
            num_weights = int(self.user_inputs[1].text())  # Ağırlık sayısını alalım
            sol_per_pop = int(
                self.user_inputs[2].text()
            )  # Popülasyon başına çözüm sayısını alalım
            low = float(self.user_inputs[3].text())  # Minimum değeri alalım
            high = float(self.user_inputs[4].text())  # Maksimum değeri alalım
            num_generations = int(
                self.user_inputs[5].text()
            )  # Jenerasyon (Nesil) sayısını alalım
            num_parents_mating = int(
                self.user_inputs[6].text()
            )  # Eşleşme için birey sayısını alalım

            # Genetik algoritmayı çalıştıralım ve sonuçları hesaplayalım
            pop_size = (sol_per_pop, num_weights)  # Popülasyon büyüklüğünü belirleyelim
            new_population = np.random.uniform(
                low=low, high=high, size=pop_size
            )  # Başlangıç popülasyonunu rastgele oluşturalım

            result_list = []  # Sonuç listesi sıfırlandı
            for generation in range(num_generations):
                # Popülasyondaki her bir kromozomun uygunluğunu hesaplayalım
                fitness = GA.cal_pop_fitness(equation_user_inputs, new_population)

                # Eşleşme havuzundaki ebeveynleri seçelim
                parents = GA.select_mating_pool(
                    new_population, fitness, num_parents_mating
                )

                # Çaprazlama ile yeni bireyler üretelim
                offspring_crossover = GA.crossover(
                    parents,
                    offspring_size=(pop_size[0] - parents.shape[0], num_weights),
                )

                # Mutasyon uygulayalım
                offspring_mutation = GA.mutation(offspring_crossover)

                # Yeni popülasyonu güncelleyelim
                new_population[0 : parents.shape[0], :] = parents
                new_population[parents.shape[0] :, :] = offspring_mutation

                # En iyi uygunluğa sahip çözümü ve uygunluğu görüntüleyelim
                fitness = GA.cal_pop_fitness(equation_user_inputs, new_population)
                best_match_idx = np.where(fitness == np.max(fitness))

                result = (
                    f"Nesil {generation + 1}: \n"  # Hangi jenerasyonda (nesilde) olduğumuzu belirtmek için
                    f"En iyi sonuç: {np.max(np.sum(new_population*equation_user_inputs, axis=1))} \n"  # En iyi sonucu belirtmek için
                    f"En iyi çözüm: {new_population[best_match_idx, :]} \n"  # En iyi çözümü göstermek için
                    f"En iyi çözüm fitness: {fitness[best_match_idx]} \n"  # En iyi çözümün uygunluğunu belirtmek için
                )
                result_list.append(result)  # Tek bir string olarak ekleme

            # Sonuçları ListView'a ekleyelim
            model = QStringListModel(result_list)
            self.result_list_view.setModel(model)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            msg_box = QMessageBox()
            msg_box.setStyleSheet(
                "background-color: #1069d8; color: white; font-weight: bold;"
            )  # Yazı rengini beyaz olarak ayarla
            msg_box.setText(error_message)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowIcon(QIcon("logo.png"))
            msg_box.exec_()

    def clearListView(self):
        # ListView'ı temizleme
        model = QStringListModel()
        self.result_list_view.setModel(model)

        # QLineEdit'ların içeriğini temizleme
        for input_field in self.user_inputs:
            input_field.clear()


def main():
    app = QApplication(sys.argv)  # PyQt5 uygulamasını başlatalım
    ex = GeneticAlgorithmUI()  # Uygulama arayüzü için bir nesne örneği oluşturalım.
    ex.showMaximized()  # Uygulama arayüzünü tam ekran olarak göstermek için
    sys.exit(
        app.exec_()
    )  # Uygulamanın ana döngüsünü başlatır ve çıkış yapana kadar çalışmasını sağlar


if __name__ == "__main__":
    main()
