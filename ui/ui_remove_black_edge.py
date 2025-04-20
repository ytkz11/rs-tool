#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_remove_black_edge.py
# time: 2025/04/17
# 黑边去除 UI
import os
from PyQt5.QtWidgets import QFrame, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from function.tools import Tool
from function.remove_black_edges_border import remove_black_edges_border_only
from resources.remove_black_edge import Ui_Form

class RemoveBlackEdgeWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(RemoveBlackEdgeWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()
        self.process_btn.setEnabled(False)  # 初始时禁用处理按钮

    def signals(self):
        """连接按钮信号"""
        self.input_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.input_filepath_line))

    def validate_input(self):
        """验证文件后缀并启用/禁用处理按钮"""
        input_path = self.input_filepath_line.text()
        output_path = self.output_filepath_line.text()

        # 检查输入路径
        input_valid = False
        if input_path:
            suffix = os.path.splitext(input_path)[1].lower()
            if suffix not in ['.tif', '.tiff']:
                self.tool.show_error(self, "❗️ 文件错误", "无效的文件后缀。仅支持 .tif 或 .tiff 文件。")
                self.TitleLabel_3.setText("无效的文件格式。请选择 .tif 或 .tiff 文件。")
            elif not os.path.exists(input_path):
                self.TitleLabel_3.setText("输入文件不存在。请提供一个有效的栅格文件路径。")
            else:
                input_valid = True
        else:
            self.TitleLabel_3.setText("请选择一个输入文件。")

        # 检查输出路径
        output_valid = True

        if input_valid and output_valid:
            self.TitleLabel_3.setText("黑边去除")
            self.process_btn.setEnabled(True)
        else:
            self.process_btn.setEnabled(False)

    def process(self):
        """处理黑边去除"""
        input_path = self.input_filepath_line.text()
        output_path = self.output_filepath_line.text()
        block_size = self.block_size_spinbox.value()
        edge_width = self.edge_width_spinbox.value()

        # 验证输入文件
        if not os.path.exists(input_path):
            self.tool.show_error(self, "❗️ 文件错误", "输入文件不存在。")
            self.TitleLabel_3.setText("输入文件不存在。请提供一个有效的栅格文件路径。")
            return

        # 验证输出文件后缀
        if os.path.splitext(output_path)[1].lower() not in ['.tif', '.tiff']:
            self.tool.show_error(self, "❗️ 文件错误", "无效的输出文件后缀。仅支持 .tif 或 .tiff 文件。")
            self.TitleLabel_3.setText("无效的输出文件格式。请选择 .tif 或 .tiff 文件。")
            return

        try:
            # 初始化进度条
            self.progressBar.setProperty("value", 0)
            self.progressBar.setMaximum(100)

            # 处理图像并使用进度回调
            def progress_callback(progress_percent):
                self.progressBar.setProperty("value", progress_percent)

            success = remove_black_edges_border_only(
                input_path,
                output_path,
                block_size=block_size,
                edge_width=edge_width,
                progress_callback=progress_callback
            )

            if success:
                self.TitleLabel_3.setText("处理成功完成！")
            else:
                self.TitleLabel_3.setText("处理失败。")
        except Exception as e:
            self.tool.show_error(self, "❗️ 处理错误", f"发生错误: {str(e)}")
            self.TitleLabel_3.setText("处理失败。请检查输入参数。")
