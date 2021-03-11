#!usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


import os
from os import path
from PyQt5.uic import loadUiType

import urllib.request
import pafy
import humanize

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()

    def InitUI(self):
        # contains all the ui changes in loading
        pass

    def Handle_Buttons(self):
        # handles all buttons in the app
        self.pushButton.clicked.connect(self.Dowload)
        self.pushButton_2.clicked.connect(self.Handle_Browse)

        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Dowload_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)

    def Handle_Progess(self, blocknum, blocksize, totalsize):
        # calculates the download progress
        read_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = read_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)

        QApplication.processEvents()

    def Handle_Browse(self):
        # enables browsing to our os, pick a save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_2.setText(str(save_location[0]))

    def Dowload(self):
        # downloading any file
        print("Download started")

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(
                    download_url, save_location, self.Handle_Progess)
            except Exception:
                QMessageBox.warning(self, "Dowload Error",
                                    "Provide a valid URL")
                return

        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Browse(self):
        # saves selected download location in the line edit
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*")

        self.lineEdit_3.setText(str(save_location[0]))

    def Get_Video_Data(self):

        video_url = self.lineEdit_4.text()
        print(video_url)

        if video_url == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL")

        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video_videostreams

            for steam in video_streams:
                print(stream.get_filesize())
                size = humanize.naturalsize(steam.get_filesize())
                data = f"{stream.mediatype} {stream.extension} {steam.quality} {size}"

                self.comboBox.addItem(data)

    def Dowload_Video(self):
        video_url = self.lineEdit_4.text()
        save_location.self.lineEdit_3.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(
                filepath=save_location, callback=self.Video_Progress)

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received

        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60, 2)

            self.label_6.setText(str(f'{remaining_time} minutes remaining'))
            QApplication.processEvents()

    def Playlist_Download(self):
        playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

            os.chdir(save_location)

            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))

            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            current_video_in_download = 1
            quality = self.comboBox_2.currentIndex()

            QApplication.processEvents()

            for video in playlist_videos:
                current_video = video['pafy']
                current_video_stream = current_video.videostreams
                self.lcdNumber.display(current_video_in_download)
                download = current_video_stream[quality].download(
                    callback=self.Playlist_Progress)

                current_video_in_download += 1

    def Playlist_Progress(self, total, received, ratio, rate, time):
        read_data = received

        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60, 2)

            self.label_5.setText(str(f'{remaining_time} minutes remaining'))
            QApplication.processEvents()

    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(
            self, "Select Download Directory")
        self.lineEdit_5.setText(playlist_save_location)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
