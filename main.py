import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import generator as gn
from PyQt5.QtCore import Qt

class App(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Generator'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 900
        
        self.setWindowTitle(self.title)
        
        self.setGeometry(self.left, self.top, self.width, self.height)

        # pola w oknie
        self.zakres_czasu = QDoubleSpinBox(self)
        self.ilosc_krokow = QSpinBox(self)
        self.amplituda = QDoubleSpinBox(self)
        self.czestotliwosc = QDoubleSpinBox(self)
        self.opis_zakresu_czestotliwosci = QLineEdit(self)
        self.opis_ilosci_krokow = QLineEdit(self)
        self.opis_amplitudy = QLineEdit(self)
        self.opis_czestotliwosci = QLineEdit(self)
        self.wykres_czasu = pg.PlotWidget(self)
        self.wykres_transformaty = pg.PlotWidget(self)
        self.radio1 = []

            # radio button
        self.radio1.append(QRadioButton('Sinus'))
        self.radio1.append(QRadioButton('Prostokąt'))
        self.radio1.append(QRadioButton('Piłokształtny'))
        self.radio1.append(QRadioButton('Trójkąt'))
        self.radio1.append(QRadioButton('Biały szum'))
        self.radio1[0].setChecked(True)

            # zakres czasu
        self.opis_zakresu_czestotliwosci.setText('Zakres czasu:')
        self.opis_zakresu_czestotliwosci.setStyleSheet("font: 40px")
        self.opis_zakresu_czestotliwosci.setReadOnly(True)
        self.opis_zakresu_czestotliwosci.setFrame(False)
        self.zakres_czasu.setFrame(False)
        self.zakres_czasu.setLineEdit(QLineEdit(self))
        self.zakres_czasu.setStyleSheet("font: 40px")
        self.zakres_czasu.setSingleStep(0.05)
        self.zakres_czasu.setMaximum(1000)
        self.zakres_czasu.setValue(1000)
           
            # ilosc krokow
        self.opis_ilosci_krokow.setText('Ilość kroków:')
        self.opis_ilosci_krokow.setReadOnly(True)
        self.opis_ilosci_krokow.setFrame(False)
        self.opis_ilosci_krokow.setStyleSheet("font: 40px")
        self.ilosc_krokow.setFrame(False)
        self.ilosc_krokow.setLineEdit(QLineEdit(self))
        self.ilosc_krokow.setStyleSheet("font: 40px")
        self.ilosc_krokow.setMaximum(10000)
        self.ilosc_krokow.setValue(10000)

            # amplituda
        self.opis_amplitudy.setText('Amplituda:')
        self.opis_amplitudy.setReadOnly(True)
        self.opis_amplitudy.setFrame(False)
        self.opis_amplitudy.setStyleSheet("font: 40px")
        self.amplituda.setFrame(False)
        self.amplituda.setLineEdit(QLineEdit(self))
        self.amplituda.setStyleSheet("font: 40px")
        self.amplituda.setSingleStep(0.01)
        self.amplituda.setMaximum(1)
        self.amplituda.setValue(1)

            # czesttliwosc
        self.opis_czestotliwosci.setText('Częstotliwość:')
        self.opis_czestotliwosci.setReadOnly(True)
        self.opis_czestotliwosci.setFrame(False)
        self.opis_czestotliwosci.setStyleSheet("font: 40px")
        self.czestotliwosc.resize(250, 50)
        self.czestotliwosc.setLineEdit(QLineEdit(self))
        self.czestotliwosc.setStyleSheet("font: 40px")
        self.czestotliwosc.setSingleStep(0.05)
        self.czestotliwosc.setMaximum(5000)
        self.czestotliwosc.setMinimum(20)
        self.czestotliwosc.setValue(440)

            # wykresy
        self.wykres_czasu.setXRange(0, 1000)
        self.wykres_czasu.setYRange(-1, 1)
        self.wykres_czasu.setLabel('left', text='<font size=15>wartosc</font>')
        self.wykres_czasu.setLabel('bottom', text='<font size=15>czas[s]</font>')
        self.wykres_transformaty.setXRange(0, 5000)
        self.wykres_transformaty.setYRange(0, 1)
        self.wykres_transformaty.setLabel('left', text='<font size=10>wartosc</font>')
        self.wykres_transformaty.setLabel('bottom', text='<font size=10>czestotliwosc[Hz]</font>')

        # dynamiczna zmiana
        self.czestotliwosc.valueChanged.connect(self.radio1_dzialanie)
        self.amplituda.valueChanged.connect(self.radio1_dzialanie)

        # pasek menu
        menu = self.menuBar()
        calculate_menu = menu.addMenu("Calculate")
        file_menu = menu.addMenu("Plik")
        zapisz = QAction('zapisz', self)
        zapisz.triggered.connect(self.save)
        file_menu.addAction(zapisz)
        lista_opcji = []
        lista_opcji.append(QAction('Sine', self))
        lista_opcji.append(QAction('Square', self))
        lista_opcji.append(QAction('Sawtooth', self))
        lista_opcji.append(QAction('Triangle', self))
        lista_opcji.append(QAction('White Noise', self))
        for i in range(0, 5):
            calculate_menu.addAction(lista_opcji[i])
        
        # wykonanie opcji
        lista_opcji[0].triggered.connect(self.Sine)
        lista_opcji[1].triggered.connect(self.Square)
        lista_opcji[2].triggered.connect(self.Sawtooth)
        lista_opcji[3].triggered.connect(self.Triangle)
        lista_opcji[4].triggered.connect(self.White_noise)

        # tabelka
        self.table = QTableWidget(self)
        self.table.resize(500, 375)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView(Qt.Horizontal).Stretch)
        self.table.setColumnCount(2)

        # layouty
        layout1 = QVBoxLayout()
        layout2_zakres_czasu = QHBoxLayout()
        layout3_ilosc_krokow = QHBoxLayout()
        layout4_amplituda = QHBoxLayout()
        layout5_czestotliwosc = QHBoxLayout()
        layout6_ploty = QHBoxLayout()
        layout7_radio = QHBoxLayout()
        for radio in self.radio1:
            layout7_radio.addWidget(radio)
            radio.toggled.connect(self.radio1_dzialanie)

        # layouty poziome
        layout2_zakres_czasu.addWidget(self.opis_zakresu_czestotliwosci)
        layout2_zakres_czasu.addWidget(self.zakres_czasu)
        layout3_ilosc_krokow.addWidget(self.opis_ilosci_krokow)
        layout3_ilosc_krokow.addWidget(self.ilosc_krokow)
        layout4_amplituda.addWidget(self.opis_amplitudy)
        layout4_amplituda.addWidget(self.amplituda)
        layout5_czestotliwosc.addWidget(self.opis_czestotliwosci)
        layout5_czestotliwosc.addWidget(self.czestotliwosc)
        layout6_ploty.addWidget(self.wykres_czasu)
        layout6_ploty.addWidget(self.wykres_transformaty)
        

        # layout pionowy
        layout1.addLayout(layout2_zakres_czasu)
        layout1.addLayout(layout3_ilosc_krokow)
        layout1.addLayout(layout4_amplituda)
        layout1.addLayout(layout5_czestotliwosc)
        layout1.addLayout(layout7_radio)
        layout1.addLayout(layout6_ploty)
        layout1.addWidget(self.table)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout1)
        self.radio1_dzialanie()
        self.show()

    def Sine(self):
        generator = gn.Generator(0, self.zakres_czasu.value(), self.ilosc_krokow.value())
        generator.sine(self.czestotliwosc.value(), self.amplituda.value())
        self.odczyt(generator)
    
    def Square(self):
        generator = gn.Generator(0, self.zakres_czasu.value(), self.ilosc_krokow.value())
        generator.square(self.czestotliwosc.value(), self.amplituda.value())
        self.odczyt(generator)
    
    def Sawtooth(self):
        generator = gn.Generator(0, self.zakres_czasu.value(), self.ilosc_krokow.value())
        generator.sawtooth(self.czestotliwosc.value(), self.amplituda.value())
        self.odczyt(generator)
    
    def Triangle(self):
        generator = gn.Generator(0, self.zakres_czasu.value(), self.ilosc_krokow.value())
        generator.triangle(self.czestotliwosc.value(), self.amplituda.value())
        self.odczyt(generator)
    
    def White_noise(self):
        generator = gn.Generator(0, self.zakres_czasu.value(), self.ilosc_krokow.value())
        generator.white_noise(self.amplituda.value())
        self.odczyt(generator) 
        
    def odczyt(self, generator):
        dane = pd.read_csv(r"function.csv", sep="\t")
        y = np.int16(dane["y"])/32767
        x = np.int16(dane["t"])
        self.table.setRowCount(len(x))
        for i in range(0, len(x)):
            self.table.setItem(i, 0, QTableWidgetItem(str(x[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(y[i])))
        self.wykres_czasu.clear()
        self.wykres_transformaty.clear()
        self.widoczny_wykres_czasu = self.wykres_czasu.plot(x, y)
        gn.Generator.save_ttf(generator, y)
        danef = pd.read_csv(r"ttf.csv", sep="\t")
        xf = np.array(danef["x"])
        yf = np.array(danef["y"])
        self.widoczny_wykres_transformaty = self.wykres_transformaty.plot(xf*10000, yf)

    def save(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.etOpenFileName()", "", options=options)
        try:
            file = open(filename, 'w')
            file.write(self.line.text())
            file.close()
        except:
            pass
    
    def radio1_dzialanie(self):
        if self.radio1[0].isChecked():
            eval('self.Sine()')
        if self.radio1[1].isChecked():
            eval('self.Square()')
        if self.radio1[2].isChecked():
            eval('self.Sawtooth()')
        if self.radio1[3].isChecked():
            eval('self.Triangle()')
        if self.radio1[4].isChecked():
            eval('self.White_noise()') 

app = QApplication(sys.argv)
ex = App()
app.exec_()