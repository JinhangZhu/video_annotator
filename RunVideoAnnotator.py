# -*- coding: utf-8 -*-
# @Time     : 2021/5/9 23:59
# @Author   : Jinhang
# @File     : RunVideoAnnotator.py
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QFileDialog

from VideoAnnotator_ui import Ui_MainWindow
from VideoPlay import Video
from utils import get_video_paths_with_places


class MainPanel(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainPanel, self).__init__()
        self.setupUi(self)

        self.source_directory_path = None
        self.video_absolute_paths = None
        self.current_video_index = None
        self.current_video_absolute_path = None
        self.video_places = None

        self.old_video_name = None
        self.new_video_name = None

        icon = QApplication.style().standardIcon(QStyle.SP_MediaPlay)
        self.pushButtonPlay.setIcon(icon)

        self.update_button_status()
        self.setupSignals()

    def update_button_status(self):
        isClickable = self.video_absolute_paths is not None
        self.pushButtonPlay.setEnabled(isClickable)
        self.pushButtonPrevious.setEnabled(isClickable)
        self.pushButtonNext.setEnabled(isClickable)

    def setupSignals(self):
        self.pushButtonPlay.clicked.connect(self.onPlay)
        self.pushButtonPrevious.clicked.connect(self.onChangeVideo)
        self.pushButtonNext.clicked.connect(self.onChangeVideo)
        self.pushButtonChooseSource.clicked.connect(self.onChooseSource)
        self.pushButtonSaveLabels.clicked.connect(self.onSaveLabels)

    def onPlay(self):
        movie = Video(self.current_video_absolute_path)
        movie.play()

    def onChangeVideo(self):
        if self.sender() == self.pushButtonPrevious:
            if self.current_video_index == 0:
                self.print_message("Reach the head of the video list!")
                return
            self.current_video_index -= 1

        else:
            if self.current_video_index == len(self.video_absolute_paths) - 1:
                self.print_message("Reach the end of the video list!")
                return
            self.current_video_index += 1

        self.update_current_video()

    def update_current_video(self):
        self.current_video_absolute_path = self.video_absolute_paths[self.current_video_index]
        self.print_message("Current video: {}".format(self.current_video_absolute_path))

    def onChooseSource(self):
        source_path = str(QFileDialog.getExistingDirectory(self, "Choose source directory where videos are"))
        if len(source_path) == 0:
            self.print_message("Empty string! Please rechoose source!")
            return
        self.source_directory_path = source_path
        self.lineEditSource.setText(source_path)

        self.video_absolute_paths, self.video_places = get_video_paths_with_places(source=self.source_directory_path,
                                                                                   endswith=['.mp4', '.m2ts', '.mts',
                                                                                             '.mov', '.3gp'])
        self.current_video_index = 0

        self.update_current_video()
        self.update_button_status()

    def onSaveLabels(self):
        pass

    def print_message(self, msg):
        self.statusbar.showMessage(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_panel = MainPanel()
    main_panel.show()
    sys.exit(app.exec_())
