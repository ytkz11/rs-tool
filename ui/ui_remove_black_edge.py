#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_remove_black_edge.py
# time: 2025/04/17
# 黑边去除 UI
import os
from PyQt5.QtWidgets import QFrame, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from function.tools import Tool
from function.remove_black_edges_border import remove_black_edges_border_only
from resources.remove_black_edge import Ui_Form

class Worker(QObject):
    """Worker class for running image processing in a separate thread"""
    progress = pyqtSignal(int)  # Signal for progress updates
    finished = pyqtSignal(bool)  # Signal for completion (success or failure)
    error = pyqtSignal(str)  # Signal for error messages

    def __init__(self, input_path, output_path, block_size, edge_width):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.block_size = block_size
        self.edge_width = edge_width

    def run(self):
        """Run the image processing task"""
        try:
            def progress_callback(progress_percent):
                self.progress.emit(int(progress_percent))

            success = remove_black_edges_border_only(
                self.input_path,
                self.output_path,
                block_size=self.block_size,
                edge_width=self.edge_width,
                progress_callback=progress_callback
            )
            self.finished.emit(success)
        except Exception as e:
            self.error.emit(str(e))

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
        self.validate_input()  # 初始验证
        self.thread = None  # Thread for image processing
        self.worker = None  # Worker for image processing

    def signals(self):
        """连接按钮信号和输入变化信号"""
        self.input_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.input_filepath_line))
        self.input_filepath_line.textChanged.connect(self.validate_input)
        self.output_filepath_line.textChanged.connect(self.validate_input)
        self.block_size_spinbox.valueChanged.connect(self.validate_input)
        self.edge_width_spinbox.valueChanged.connect(self.validate_input)

    def validate_input(self):
        """验证输入和输出路径、分块尺寸、边宽，并控制处理按钮的启用状态"""
        input_path = self.input_filepath_line.text().strip()
        output_path = self.output_filepath_line.text().strip()
        block_size = self.block_size_spinbox.value()
        edge_width = self.edge_width_spinbox.value()

        # 检查输入路径
        input_valid = False
        if input_path:
            suffix = os.path.splitext(input_path)[1].lower()
            if suffix not in ['.tif', '.tiff']:
                self.TitleLabel_3.setText("无效的输入文件格式。请选择 .tif 或 .tiff 文件。")
            elif not os.path.exists(input_path):
                self.TitleLabel_3.setText("输入文件不存在。请提供一个有效的栅格文件路径。")
            else:
                input_valid = True
        else:
            self.TitleLabel_3.setText("请选择一个输入文件。")

        # 检查输出路径
        output_valid = False
        if output_path:
            suffix = os.path.splitext(output_path)[1].lower()
            if suffix not in ['.tif', '.tiff']:
                self.TitleLabel_3.setText("无效的输出文件格式。请选择 .tif 或 .tiff 文件。")
            elif not os.path.exists(os.path.dirname(output_path)) and os.path.dirname(output_path):
                self.TitleLabel_3.setText("输出目录不存在。请提供一个有效的目录。")
            else:
                output_valid = True
        else:
            self.TitleLabel_3.setText("请选择一个输出文件。")

        # 检查输入和输出路径是否相同
        paths_different = True
        if input_valid and output_valid and input_path == output_path:
            self.TitleLabel_3.setText("输入和输出文件路径不能相同。")
            paths_different = False

        # 检查分块尺寸和边宽
        params_valid = block_size > 0 and edge_width > 0
        if not params_valid:
            self.TitleLabel_3.setText("分块尺寸和边宽必须大于 0。")

        # 所有条件都满足时启用处理按钮
        if input_valid and output_valid and paths_different and params_valid:
            self.TitleLabel_3.setText("黑边去除")
            self.process_btn.setEnabled(True)
        else:
            self.process_btn.setEnabled(False)

    def process(self):
        """处理黑边去除（在单独线程中运行）"""
        input_path = self.input_filepath_line.text().strip()
        output_path = self.output_filepath_line.text().strip()
        block_size = self.block_size_spinbox.value()
        edge_width = self.edge_width_spinbox.value()

        # 最终验证
        if not os.path.exists(input_path):
            self.tool.show_error(self, "❗️ 文件错误", "输入文件不存在。")
            self.TitleLabel_3.setText("输入文件不存在。请提供一个有效的栅格文件路径。")
            return False

        if os.path.splitext(input_path)[1].lower() not in ['.tif', '.tiff']:
            self.tool.show_error(self, "❗️ 文件错误", "无效的输入文件后缀。仅支持 .tif 或 .tiff 文件。")
            self.TitleLabel_3.setText("无效的输入文件格式。请选择 .tif 或 .tiff 文件。")
            return False

        if os.path.splitext(output_path)[1].lower() not in ['.tif', '.tiff']:
            self.tool.show_error(self, "❗️ 文件错误", "无效的输出文件后缀。仅支持 .tif 或 .tiff 文件。")
            self.TitleLabel_3.setText("无效的输出文件格式。请选择 .tif 或 .tiff 文件。")
            return False

        if input_path == output_path:
            self.tool.show_error(self, "❗️ 文件错误", "输入和输出文件路径不能相同。")
            self.TitleLabel_3.setText("输入和输出文件路径不能相同。")
            return False

        if not os.path.exists(os.path.dirname(output_path)) and os.path.dirname(output_path):
            self.tool.show_error(self, "❗️ 文件错误", "输出目录不存在。")
            self.TitleLabel_3.setText("输出目录不存在。")
            return False

        if block_size <= 0 or edge_width <= 0:
            self.tool.show_error(self, "❗️ 参数错误", "分块尺寸和边宽必须大于 0。")
            self.TitleLabel_3.setText("分块尺寸和边宽必须大于 0。")
            return False

        # 禁用处理按钮以防止重复点击
        self.process_btn.setEnabled(False)
        self.TitleLabel_3.setText("正在处理，请稍候...")

        # 初始化进度条
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMaximum(100)

        # 创建线程和工作者
        self.thread = QThread()
        self.worker = Worker(input_path, output_path, block_size, edge_width)

        # 将工作者移动到线程
        self.worker.moveToThread(self.thread)

        # 连接信号
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 启动线程
        self.thread.start()
        return True

    def on_processing_finished(self, success):
        """处理完成时的回调"""
        self.process_btn.setEnabled(True)  # 重新启用处理按钮
        if success:
            self.TitleLabel_3.setText("处理成功完成！")
            QMessageBox.information(self, "成功", "黑边去除处理完成！")
        else:
            self.TitleLabel_3.setText("处理失败。")
            self.tool.show_error(self, "❗️ 处理错误", "黑边去除处理失败。")
        self.thread.quit()
        self.thread.wait()

    def on_processing_error(self, error_message):
        """处理错误时的回调"""
        self.process_btn.setEnabled(True)  # 重新启用处理按钮
        self.tool.show_error(self, "❗️ 处理错误", f"发生错误: {error_message}")
        self.TitleLabel_3.setText("处理失败。请检查输入参数。")
        self.thread.quit()
        self.thread.wait()