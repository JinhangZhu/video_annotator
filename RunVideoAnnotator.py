# -*- coding: utf-8 -*-
# @Time     : 2021/5/9 23:59
# @Author   : Jinhang
# @File     : RunVideoAnnotator.py
import os
import sys

from PyQt5.QtCore import Qt
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

        self.all_checkboxes = [self.checkBox_me,
                               self.checkBox_bird,
                               self.checkBox_food,
                               self.checkBox_sky,
                               self.checkBox_field,
                               self.checkBox_buildingin,
                               self.checkBox_buildingout,
                               self.checkBox_specialevent,
                               self.checkBox_specialspot,
                               self.checkBox_walkanimal,
                               self.checkBox_local,
                               self.checkBox_pal]

        icon = QApplication.style().standardIcon(QStyle.SP_MediaPlay)
        self.pushButtonPlay.setIcon(icon)

        self.update_button_status()
        self.setupSignals()

    def update_button_status(self):
        isClickable = self.video_absolute_paths is not None
        self.pushButtonPlay.setEnabled(isClickable)
        self.pushButtonPrevious.setEnabled(isClickable)
        self.pushButtonNext.setEnabled(isClickable)
        self.pushButtonSaveLabels.setEnabled(isClickable)

        for check_box in self.all_checkboxes:
            check_box.setCheckable(isClickable)

    def setupSignals(self):
        self.pushButtonPlay.clicked.connect(self.onPlay)
        self.pushButtonPrevious.clicked.connect(self.onPreviousVideo)
        self.pushButtonNext.clicked.connect(self.onNextVideo)
        self.pushButtonChooseSource.clicked.connect(self.onChooseSource)
        self.pushButtonSaveLabels.clicked.connect(self.onSaveLabels)

        for check_box in self.all_checkboxes:
            check_box.stateChanged.connect(self.onChangeNewName)

    def onPlay(self):
        movie = Video(self.current_video_absolute_path)
        movie.play()

    def onPreviousVideo(self):
        if self.current_video_index == 0:
            self.print_message("Reach the head of the video list!")
            return
        self.current_video_index -= 1
        self.update_current_video()

    def onNextVideo(self):
        if self.current_video_index == len(self.video_absolute_paths) - 1:
            self.print_message("Reach the end of the video list!")
            return
        self.current_video_index += 1
        self.update_current_video()

    def update_current_video(self):
        self.current_video_absolute_path = self.video_absolute_paths[self.current_video_index]
        self.print_message("Current video: {}".format(self.current_video_absolute_path))

        base_name = os.path.basename(self.current_video_absolute_path)
        self.new_video_name = base_name
        self.lineEditNewName.setText(self.new_video_name)

    def onChooseSource(self):
        source_path = str(
            QFileDialog.getExistingDirectory(self, "Choose source directory where videos are", 'G:/Pictures'))
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
        dir_name = os.path.dirname(self.current_video_absolute_path)
        new_file_name = dir_name + '/' + self.new_video_name

        os.rename(self.current_video_absolute_path, new_file_name)
        self.print_message("Rename as: {}".format(new_file_name))

        self.video_absolute_paths[self.current_video_index] = new_file_name
        self.update_current_video()

    def onChangeNewName(self):
        if self.new_video_name is None:
            return

        base_name_without_extension, extension = os.path.splitext(self.new_video_name)
        print('File: {} Extension: {}'.format(base_name_without_extension, extension))

        for check_box in self.all_checkboxes:
            if self.sender() == check_box:
                if check_box.isChecked():
                    base_name_without_extension += '_{}'.format(check_box.text())
                else:
                    base_name_without_extension = base_name_without_extension.replace(
                        '_{}'.format(check_box.text()), '')

        self.new_video_name = base_name_without_extension + extension
        self.lineEditNewName.setText(self.new_video_name)

    def keyPressEvent(self, event) -> None:
        if self.video_absolute_paths is None:
            return
        if event.key() == Qt.Key_F1:
            self.onPreviousVideo()
        if event.key() == Qt.Key_F2:
            self.onNextVideo()

    def print_message(self, msg):
        self.statusbar.showMessage(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_panel = MainPanel()
    main_panel.show()
    sys.exit(app.exec_())
