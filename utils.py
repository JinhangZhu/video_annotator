# -*- coding: utf-8 -*-
# @Time     : 2021/5/10 0:31
# @Author   : Jinhang
# @File     : utils.py

import os


def get_video_paths_with_places(source, endswith=None):
    if endswith is None:
        endswith = ['.mp4', '.m2ts', '.mts', '.mov', '.3gp']
    need_paths = []
    all_extensions = []
    need_extensions = []
    need_places = []

    # r=root, d=directories, f = files
    for root, dirs, files in os.walk(source):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension not in all_extensions:
                all_extensions.append(file_extension)

            for end in endswith:
                if file.endswith(end.lower()) or file.endswith(end.upper()):
                    abs_path = os.path.join(root, file)
                    abs_path = abs_path.replace('\\', '/')

                    need_paths.append(abs_path)
                    need_places.append(abs_path.split('/')[2])
                    if file_extension not in need_extensions:
                        need_extensions.append(file_extension)

    print("\n{} videos are found with {} types of extensions: {}".format(len(need_paths), len(need_extensions), need_extensions))
    print("\nAmong all files are {} types of extensions: {}".format(len(all_extensions), all_extensions))

    return need_paths, need_places


if __name__ == '__main__':
    need_paths, need_places = get_video_paths_with_places(source='G:/Pictures', endswith=['.mp4', '.m2ts', '.mts', '.mov', '.3gp'])
