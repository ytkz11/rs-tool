#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_color_enhance.py
# time: 2024/9/11 20:12
# 按属性分层
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from function.tools import Tool
from function.color_enhancement import ColorEnhancement
from resources.color_enhanmence import Ui_Form
import re
def is_numeric(value):
    return bool(re.match(r'^[+-]?(\d+(\.\d*)?|\.\d+)$', value))
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

class color_enhanceWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(color_enhanceWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()
        self.color_process_btn.setEnabled(False)

    def signals(self):
        """按钮触发， 主动调用"""
        self.color_enhance_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.color_enhance_filepath_line))
        self.color_enhance_filepath_line.textChanged.connect(self.suffix_info)

        self.color_lineEdit.textChanged.connect(self.suffix_value_info)


    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.color_enhance_filepath_line)

        value = self.color_lineEdit.text()
        if os.path.exists(self.tool.path) ==False:
            self.tool.show_error(self, "❗️文件夹错误", "文件夹不存在")
            self.color_process_btn.setEnabled(False)
        else:
            tif_list = get_file_name(self.tool.path, ['.TIF', '.tif', '.TIFF', '.tiff'])
            if len(tif_list) >0:
                self.tool.show_message("文件夹下存在栅格", str(tif_list))
                if is_numeric(value):
                    self.color_process_btn.setEnabled(True)

    def suffix_value_info(self):
        value = self.color_lineEdit.text()
        if is_numeric(value) == False:
            self.color_process_btn.setEnabled(False)
        else:
            if float(value) > 1 or float(value) < 0:
                self.tool.show_error(self, "❗️数值错误", "请输入阈值范围在0-1之间")
                self.color_process_btn.setEnabled(False)
            else:
                tif_list = get_file_name(self.tool.path, ['.TIF', '.tif', '.TIFF', '.tiff'])
                if len(tif_list) > 0:
                    self.color_process_btn.setEnabled(True)
    def process(self):
        """处理"""

        if self.tool.path:
            # self.header_box_clear()
            tif_list = get_file_name(self.tool.path, ['.TIF', '.tif', '.TIFF', '.tiff'])
            value = float(self.color_lineEdit.text())
            self.color_process_btn.setEnabled(False)
            self.color_process_btn.setText('正在进行植被色彩增强')
            for i, file in enumerate(tif_list):
                ColorEnhancement(file, value = value).process()
                self.progressBar.setValue((i+1)/len(tif_list))
                print(file)
            self.color_process_btn.setEnabled(True)
            self.color_process_btn.setText('完成进行植被色彩增强')


