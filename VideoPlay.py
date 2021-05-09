# -*- coding: utf-8 -*-
# @Time     : 2021/5/9 23:25
# @Author   : Jinhang
# @File     : VideoPlay.py

class Video(object):
    def __init__(self, path):
        self.path = path

    def play(self):
        from os import startfile
        startfile(self.path)


if __name__ == '__main__':
    import os
    abs_path = os.path.abspath('resource/video.mp4')
    movie = Video(abs_path)
    if input("Press enter to play, anything else to exit") == '':
        movie.play()
