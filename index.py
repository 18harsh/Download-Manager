from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
import os
from os import path
import humanize


ui,_ = loadUiType('downloads.ui')

class MainApp(QMainWindow , ui):
	def __init__(self, parent=None):
		super(MainApp , self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.InitUI()
		self.Handle_Buttons()

	def InitUI(self):
		self.tabs.tabBar().setVisible(False)

		self.apply_dark()
		self.Move_Box_1()
		self.Move_Box_2()
		self.Move_Box_3()
		self.Move_Box_4()


	def Handle_Buttons(self):
		self.downloadButton.clicked.connect(self.Download)
		self.browseButton.clicked.connect(self.Handle_Browse)
		self.tab2downloadButton.clicked.connect(self.Download_Video)
		self.gButton.clicked.connect(self.get_video_data)
		self.bButton.clicked.connect(self.Save_Browser)
		self.tab2downloadButton_2.clicked.connect(self.Playlist_Download)
		self.bButton_2.clicked.connect(self.Save_Browser2)
		self.pushButton.clicked.connect(self.open_home)
		self.pushButton_2.clicked.connect(self.open_setting)
		self.pushButton_3.clicked.connect(self.open_youtube)
		self.pushButton_4.clicked.connect(self.open_download)
		self.pushButton_5.clicked.connect(self.apply_classic)
		self.pushButton_6.clicked.connect(self.apply_darkgray)
		self.pushButton_7.clicked.connect(self.apply_dark)
		self.pushButton_8.clicked.connect(self.apply_darkblue)

	def Handle_Progress(self , blocknum,blocksize ,totalsize):
		readed_data = blocknum*blocksize
		if totalsize>0:
			download_percentage = readed_data*100/totalsize
			self.progressBartab1.setValue(download_percentage)
			QApplication.processEvents()

		
	
	def Handle_Browse(self):
		save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory="." ,filter="All Files(*.*)")
		self.browseentry.setText(save_location[0])
	
	def Download(self):
		download_url = self.linkentry.text()
		save_location = self.browseentry.text()
		
		if download_url == "" or save_location =="":
			QMessageBox.warning(self, "Date Error", 'Provide a valid url or save location')
		else:
			try:
				urllib.request.urlretrieve(download_url, save_location , self.Handle_Progress)
			except Exception:
				QMessageBox.warning(self, "Download Error", 'Provide a valid url or save location')	
				return
		QMessageBox.information(self, "Download info", 'Download Completed')
		self.linkentry.setText("")
		self.browseentry.setText("")
		self.progressBartab1.setValue(0)

	def Save_Browser(self):
		save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory="." ,filter="All Files(*.*)")
		self.tab2locatioentry.setText(save_location[0])	

	def get_video_data(self):
		video_url = self.tab2urlentry.text()

		if video_url == "":
			QMessageBox.warning(self, "Data Error", 'Provide a valid Video URL')
		else:
			try:	
				video =pafy.new(video_url)
				video_streams =video.videostreams
				for stream in video_streams:
					size = humanize.naturalsize(stream.get_filesize())
					data = '{} {} {} {}'.format(stream.mediatype , stream.extension,stream.quality,size)
					self.tab2comboBox.addItem(data)
			
			except Exception:
				QMessageBox.warning(self, "Link Error", 'Provide a valid Video URL')

	def Download_Video(self):
		video_url = self.tab2urlentry.text()
		save_location = self.tab2locatioentry.text()

		if video_url == "" or save_location =="":
			QMessageBox.warning(self, "Date Error", 'Provide a valid url or save location')
		else:
			try:
				video = pafy.new(video_url)
				video_stream = video.videostreams
				video_quality = self.tab2comboBox.currentIndex()
				download = video_stream[video_quality].download(filepath=save_location,callback=self.Video_Progress)

			except Exception:
				QMessageBox.warning(self, "Download Error", 'Provide a valid url or save location')	
				return
		QMessageBox.information(self, "Download info", 'Download Completed')
		self.tab2urlentry.setText("")
		self.tab2locatioentry.setText("")
		self.progressBartab2_1.setValue(0)
		self.label_3.setText("")



	def Video_Progress(self,total, received,ratio,rate,time):
		read_data = received
		if total>0:
			download_percentage = read_data*100/total
			self.progressBartab2_1.setValue(download_percentage)
			remaining_time = round(time/60,2)
			self.label_3.setText('{} minutes remaining'.format(remaining_time))
			QApplication.processEvents()

	#tab2urlentry_2
	#tab2locatioentry_2
	#tab2comboBox_2
	#lcdNumber 
	#lcdNumber_2
	#progressBartab2_2
	#tab2downloadButton_2
	#bButton_2
	
	def Playlist_Download(self):
		playlist_url = self.tab2urlentry_2.text()
		save_location = self.tab2locatioentry_2.text()
		if playlist_url == '' or save_location == '':
			QMessageBox.warning(self,"Date Error",'Provide a valid Playlist URL or save location')
		else:
			playlist = pafy.get_playlist(playlist_url)
			playlist_video = playlist['items']
			self.lcdNumber_2.display(len(playlist_video))

		os.chdir(save_location)
		if os.path.exists(str(playlist['title'])):
			os.chdir(str(playlist['title']))

		else:
			os.mkdir(str(playlist['title']))
			os.chdir(str(playlist['title']))

		current_video_in_download = 1
		quality = self.tab2comboBox_2.currentIndex()
		self.lcdNumber.display(current_video_in_download)
		for video in playlist_video:
			current_video = video['pafy']
			current_video_stream = current_video.videostreams
			download = current_video_stream[quality].download(callback=self.Playlist_Progress)
			QApplication.processEvents()
			current_video_in_download +=1
			self.lcdNumber.display(current_video_in_download)


	def Playlist_Progress(self,total, received,ratio,rate,time):
		read_data = received
		if total>0:
			download_percentage = read_data*100/total
			self.progressBartab2_2.setValue(download_percentage)
			remaining_time = round(time/60,2)
			self.label_4.setText('{} minutes remaining'.format(remaining_time))
			QApplication.processEvents()

	def Save_Browser2(self):
		save_location = QFileDialog.getExistingDirectory(self, caption="Select Download Location" )
		self.tab2locatioentry_2.setText(save_location)

	def open_home(self):
		self.tabs.setCurrentIndex(0)
		self.Move_Box_1()
		self.Move_Box_2()
		self.Move_Box_3()
		self.Move_Box_4()

	def open_download(self):
		self.tabs.setCurrentIndex(1)

	def open_youtube(self):
		self.tabs.setCurrentIndex(2)

	def open_setting(self):
		self.tabs.setCurrentIndex(3)

	def apply_dark(self):
		style = open("themes/qdark.css",'r')
		style = style.read()
		self.setStyleSheet(style)

	def apply_darkgray(self):
		style = open("themes/qdarkgray.css",'r')
		style = style.read()
		self.setStyleSheet(style)


	def apply_classic(self):
		style = open("themes/classic.css",'r')
		style = style.read()
		self.setStyleSheet(style)
	
	def apply_darkblue(self):
		style = open("themes/darkblue.css",'r')
		style = style.read()
		self.setStyleSheet(style)

	def Move_Box_1(self):
		box_animation1 = QPropertyAnimation(self.groupBox,b"geometry")
		box_animation1.setDuration(1000)
		box_animation1.setStartValue(QRect(0,0,0,0))
		box_animation1.setEndValue(QRect(40,40,281,121))
		box_animation1.start()
		self.box_animation1 = box_animation1

	def Move_Box_2(self):
		box_animation2 = QPropertyAnimation(self.groupBox_2,b"geometry")
		box_animation2.setDuration(1000)
		box_animation2.setStartValue(QRect(0,0,0,0))
		box_animation2.setEndValue(QRect(360,40,281,121))
		box_animation2.start()
		self.box_animation2 = box_animation2
	
	def Move_Box_3(self):
		box_animation3 = QPropertyAnimation(self.groupBox_3,b"geometry")
		box_animation3.setDuration(1000)
		box_animation3.setStartValue(QRect(0,0,0,0))
		box_animation3.setEndValue(QRect(40,200,281,121))
		box_animation3.start()
		self.box_animation3 = box_animation3

	def Move_Box_4(self):
		box_animation4 = QPropertyAnimation(self.groupBox_4,b"geometry")
		box_animation4.setDuration(1000)
		box_animation4.setStartValue(QRect(0,0,0,0))
		box_animation4.setEndValue(QRect(360,200,281,121))
		box_animation4.start()
		self.box_animation4 = box_animation4			

def main():
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__=="__main__":
	main()