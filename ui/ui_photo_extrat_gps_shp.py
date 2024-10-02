#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_restoreshp.py
# time: 2024/9/16 23:12
# 照片提取地理信息到shp文件
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from function.tools import Tool
from function.photo_extrat_gps_shp import photo_extract_gps_info_to_shp
from resources.photo_to_gps_shp import Ui_Form
def get_file_name(file_dir, type1):
    """
        搜索 后缀名为type的文件  不包括子目录的文件
        #
        """
    L = []
    if type(type1) == str:
        if len([type1]) == 1:
            filelist = os.listdir(file_dir)
            for file in filelist:
                if os.path.splitext(file)[1] == type1:
                    L.append(os.path.join(file_dir, file))
    if type(type1) != str:
        if len(type1) > 1:
            for i in range(len(type1)):
                filelist = os.listdir(file_dir)
                for file in filelist:
                    if os.path.splitext(file)[1] == type1[i]:
                        L.append(os.path.join(file_dir, file))
    return L
class photo_extrat_gps_shpWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(photo_extrat_gps_shpWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()
        self.photo_to_gps_shp_process_btn.setEnabled(False)
    def signals(self):
        """按钮触发， 主动调用"""
        self.photo_to_gps_shp_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.restoreshp_filepath_line))
        self.photo_to_gps_shp_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.photo_to_gps_shp_filepath_line)


        if os.path.exists(self.tool.path) ==False:
            self.tool.show_error(self, "❗️文件夹错误", "文件夹不存在")
            self.photo_to_gps_shp_process_btn.setEnabled(False)
        else:
            jpg_list = get_file_name(self.tool.path, ['.JPG', '.jpg'])
            if len(jpg_list) >0:
                self.tool.show_message("文件夹下存在照片")

                self.photo_to_gps_shp_process_btn.setEnabled(True)

    def process(self):
        """处理"""

        if self.tool.path:
            # self.header_box_clear()
            # jpg_list = get_file_name(self.tool.path, ['.JPG', '.jpg', '.PNG', '.png'])

            self.photo_to_gps_shp_process_btn.setEnabled(False)
            self.photo_to_gps_shp_process_btn.setText('正在读取照片地理信息')
            photos = {}
            # photo_dir = ".\photos"
            photo_extract_gps_info_to_shp(photos, self.tool.path)

            self.photo_to_gps_shp_process_btn.setEnabled(True)
            self.photo_to_gps_shp_process_btn.setText('开始')

