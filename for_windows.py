#importing libraries
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
from sys import argv
import pafy
from pydub import AudioSegment
from os import chdir , remove , listdir , rename , mkdir
import eyed3 
from shutil import move
from time import sleep

#adding the gui file to the project
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"C:\zizo\projects/PYTHON/My_Downloader/main.ui"))

#the main class of the project
class mainapp(QMainWindow,FORM_CLASS):
    def __init__(self, parent=None):
        super(mainapp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.button_setup()
        self.ui_init()

    def button_setup(self):
        self.process_button.clicked.connect(self.procceed)
        self.download_button.clicked.connect(self.change)

    def ui_init(self):
        self.song_name.hide()
        self.artist.hide()
        self.file_size.hide()
        self.status.hide()
        self.progressBar.hide()

    def procceed(self):
        """ A Function to process song link a get information """
        #requesting song information from source
        self.songlink = self.song_link.text()
        self.song = pafy.new(self.songlink)
        self.stream = self.song.getbestaudio(preftype=("m4a"))

        #getting song tags from source
        self.songname = self.song.title.upper()
        self.song_author = self.song.author.upper()
        self.song_size = self.stream.get_filesize()
        self.size = str(self.song_size/1024/1024)

        #Displaying song tags for user
        self.song_name.setText(f"Song : {self.songname}")
        self.artist.setText(f"Artist : {self.song_author}")
        self.file_size.setText(f"File Size : {self.size[:3]} MB")
        self.song_name.show()
        self.artist.show()
        self.file_size.show()

    def change(self):      
        self.song_name.hide()
        self.artist.hide()
        self.file_size.hide()
        self.status.show()
        self.status.setText("Downloading. . . .")
        self.timer = QTimer()
        self.timer.singleShot(4000,self.download)  

    def progressbar(self,total,recvd,ratio,rate,eta):
        """A Function to deal with the progress Bar"""

        self.progressBar.show()
        self.progressBar.setValue(ratio * 100)

    def download(self):
        """The Function which Downloads the song and change its Tags and move it to its folder"""

        chdir("C:\zizo\songs_before")
        #Starting Donwload
        self.stream.download(callback=self.progressbar)
        self.status.setText("Processing. . . .")

        #changing the
        if "VEVO" in self.song_author.upper():
            m = self.song_author.find("VEVO")
            author = self.song_author.upper()[:m]
        try:
            m4song = listdir()[0]
        except IndexError:
            self.status.setText("Try another song")
        else:    
            m4songaf = m4song[:-4]
            mp3song = f"{m4songaf}.mp3"

            m4audio = AudioSegment.from_file(m4song , format="m4a")
            m4audio.export(f"{mp3song}" , format="mp3")
            
            remove(m4song)


            if "(" in self.songname:
                mo1 = self.songname.find("(")
                mo2 = self.songname.find(")")
                moh = self.songname[mo1:mo2+1]
                self.songname = self.songname[:mo1]

            if "|" in self.songname:
                index = self.songname.find("|")
                self.songname = self.songname[:index]


            #Tagging the song
            file = eyed3.load(mp3song)
            file.tag.artist = self.song_author.upper()
            file.tag.album = self.song_author.upper()
            file.tag.album_artist = self.song_author.upper()
            file.tag.title = self.songname.upper()
            file.tag.save()

            rename(mp3song,f"{self.songname}.mp3")

            chdir("C:\zizo\songs/")

            current_files = listdir()

            if self.song_author in current_files:
                move(f"C:\zizo\songs_before//{self.songname.upper()}.mp3",f"C:\zizo\songs/{self.song_author.upper()}/{self.songname.upper()}.mp3")

            else:
                mkdir(f"C:\zizo\songs/{self.song_author.upper()}")
                move(f"C:\zizo\songs_before/{self.songname.upper()}.mp3",f"C:\zizo\songs/{self.song_author.upper()}/{self.songname.upper()}.mp3")

            self.status.setText("Done :)")
            self.timer.singleShot(2500,self.init_for_recall)


    def init_for_recall(self):
        """ Function to initialize the program for a new song """
        self.song_link.setText("")
        self.status.hide()
        self.progressBar.hide()
        self.progressBar.setValue(0)



if __name__ == "__main__":
    app = QApplication(argv)
    MainWindow = QMainWindow()
    window = mainapp()
    window.show()
    app.exec()