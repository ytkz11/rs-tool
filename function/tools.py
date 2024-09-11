from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import FluentWindow, InfoBar, InfoBarPosition, ComboBox
from qfluentwidgets import Dialog


class Tool(FluentWindow):

    def __init__(self):
        super(Tool, self).__init__()
        self.path = None
        self.suffix = None

    def prompt(self, widget_btn, title, content):
        """提示信号"""
        widget_btn.clicked.connect(
            lambda: self.show_message(title=title, content=content))

    def show_message(self, title, content):
        """提示弹窗"""
        d = Dialog(title, content, self)
        if d.exec():
            pass
        else:
            pass

    def get_widget_text(self, widget):
        """获取组件text"""
        widget_list = []
        for value in widget.children():
            if isinstance(value, ComboBox):
                widget_list.append(value.text())
        return widget_list

    def get_text(self, ui_text):
        """获取文本"""
        return ui_text.text()

    def handle_path(self, ui_line):
        """处理路径"""
        self.get_file_path(ui_line)  # 写入其他路径

    def get_suffix(self, ui_line):
        """判断后缀"""
        self.path = ui_line.text()  # 获取路径
        self.suffix = Path(self.path).suffix

    def handle_csv_path(self, widget_line):
        """处理获取数据"""
        self.path = widget_line.text()

    def get_file_path(self, widget_line_name):
        """保存路径+名称"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "选择文件", "",
                                                   "All Files (*);;Text Files (*.shp)",
                                                   options=options)
        if file_name:
            widget_line_name.setText(file_name)

    def get_full_path(self, widget_line_name):

            """获取文件夹路径"""
            options = QFileDialog.Options()
            dir_name = QFileDialog.getExistingDirectory(None, "选择文件夹", "",
                                                        options=options)
            if dir_name:
                widget_line_name.setText(dir_name)

    @staticmethod
    def show_success(self):
        """在主线程中执行 InfoBar.success"""
        InfoBar.success(
            title='√操作成功',
            content="数据解析完成。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    @staticmethod
    def show_warn(self):
        InfoBar.warning(
            title='×缺少参数',
            content="请检查参数完整性。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    @staticmethod
    def show_error(self, title, content):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

