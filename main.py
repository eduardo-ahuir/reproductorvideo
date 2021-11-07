#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QSlider,QStyle,QSizePolicy,QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon,QPalette
from PyQt5.QtCore import Qt,QUrl
import apitiempo
import logging



class ventana(QWidget):
    def __init__(self):
        super().__init__()

        logging.basicConfig(filename='errores.log', encoding='utf-8', level=logging.DEBUG)
        logging.info('aplicacion iniciada')

        self.setWindowTitle("reproductor multimedia")
        self.setGeometry(350,100,700,500)
        self.setWindowIcon(QIcon('iconos/media-play-icon-19.jpg'))
        p =self.palette()
        p.setColor(QPalette.Window,Qt.black)
        self.setPalette(p)
        #variable para manejar la cantidad de veces que se ha pulsado el boton de ver el tiempo
        self.contadortiempo=1



        self.init_ui()


        self.show()

    def init_ui(self):

        self.mediaPlayer=QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget=QVideoWidget()

        botonabrir=QPushButton("open file")
        botonabrir.clicked.connect(self.open_file)




        #crea el boton reproducir y cuando es pulsado ejecuta el metodo reproducirvideo
        self.reproducir=QPushButton()
        self.reproducir.setEnabled(False)
        self.reproducir.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.reproducir.clicked.connect(self.reproducirvideo)

        #crea el slider para adelantar o atrasar el video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        self.label=QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)

        #crea el boton que sirve para usar la api "https://openweathermap.org/"
        self.botontiempo = QPushButton()
        self.botontiempo.setText("press me to know the time in "+""+apitiempo.ciudad)
        self.botontiempo.clicked.connect(self.cambiar_tiempo)
        self.botontiempo.clicked.connect(self.aumentacontador)



        #crea el slider para manejar el volumen
        self.barra_volumen = QSlider(Qt.Horizontal)
        self.barra_volumen.setRange(0, 100)
        self.barra_volumen.setValue(self.mediaPlayer.volume())
        self.barra_volumen.sliderMoved.connect(self.mediaPlayer.setVolume)




        hboxlayout=QHBoxLayout()
        hboxlayout.setContentsMargins(0,0,0,0)

        #añade los elementos correspondientes al layout
        hboxlayout.addWidget(botonabrir)
        hboxlayout.addWidget(self.reproducir)
        hboxlayout.addWidget(self.slider)
        hboxlayout.addWidget(self.barra_volumen)

        # añade los elementos correspondientes al layout
        vboxlayout=QVBoxLayout()
        vboxlayout.addWidget(videowidget)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.label)
        vboxlayout.addWidget(self.botontiempo)


        self.setLayout(vboxlayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        #crea las señales del objeto mediaplayer
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)


    #metodo para dar funcionalidad al boton de abrir archivo
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.reproducir.setEnabled(True)

    def reproducirvideo(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    #si el video se esta reproduciendo cambia el icono del boton de reproducir
    def mediastate_changed(self,state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.reproducir.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

        else:
            self.reproducir.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self,position):
        self.slider.setValue(position)

    def duration_changed(self,duration):
        self.slider.setRange(0,duration)

    def set_position(self,position):
        self.mediaPlayer.setPosition(position)

    #usando la clase apitiempo da el tiempo de una ciudad y cambia el mensaje del boton cada vez que se pulsa
    def cambiar_tiempo(self):
        print(self.contadortiempo)

        if self.contadortiempo==1:
            self.botontiempo.setText("humidity in " + str(apitiempo.ciudad) + "" + str(""+apitiempo.humedad))
        if  self.contadortiempo == 2:
            self.botontiempo.setText("preasure in " + str(apitiempo.ciudad) + " " + str(apitiempo.presion)+"Pa")
        if self.contadortiempo == 3:
            self.botontiempo.setText("time prevision in " + str(apitiempo.CITY) + "time " + str(apitiempo.tiempo))
        if self.contadortiempo == 4:
            self.botontiempo.setText("This is the time in " + str(apitiempo.CITY))
        if self.contadortiempo>4:
            logging.info('el contador es mas de 4')
    #aumenta el contador en uno para usar el metodo de arriba
    def aumentacontador(self):
        self.contadortiempo+=1
        if self.contadortiempo==5:
            self.botontiempo.setText("press me to know the time in" + apitiempo.ciudad)
            self.contadortiempo = 1






    #comprueba si ha ahbido algun error y de ser asi lo notifica
    def handle_errors(self):
        self.reproducir.setEnabled(False)
        self.label.setText("Error: "+ self.mediaPlayer.errorString())
        if apitiempo.errores==1:
            self.label.setText("error no hay conexión a internet por favor revisa tu conexión y vulve a intentarlo")
            logging.info('no hay conexion')






app = QApplication(sys.argv)
Ventana=ventana()
sys.exit(app.exec())
logging.info('aplicacion finalizada')