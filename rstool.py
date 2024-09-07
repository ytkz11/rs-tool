# - coding:utf-8 -

"""备份new_run文件"""
from new_func.messages import Content
from PyQt5.QtGui import QIcon
from qfluentwidgets import (FluentWindow, NavigationItemPosition, Flyout, FlyoutAnimationType)
from qfluentwidgets import FluentIcon as FIF
from new_func.ui_shp2dxf import shp2dxfWidget
from new_func.ui_shp2dxf_origin import shp2dxfWidget_origin
from new_func.ui_document import DocumentWidget
from new_func.tools import Tool
from new_func.ui_thread import Worker
from PyQt5.QtWidgets import QApplication

from resources.Flyout_ import CustomFlyoutView
from osgeo import ogr

class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.tool = Tool()


        self.Shp2dxf = shp2dxfWidget('shp2dxf_ui', self)
        self.Shp2dxf_origin = shp2dxfWidget_origin('shp2dxf_origin_ui', self)


        # self.Filter = FilterWidget('filter_ui', self)
        self.Document = DocumentWidget("document_ui", self)
        # self.Excel = ExcelWidget("excel_ui", self)

        """初始化界面"""
        self.success_fired = False
        self.warn_fired = False
        self.error_fired = False
        self.init_navigation()
        # self.add_loading_ui()
        self.click_prompt_signal()
        self.window_signals()
        self.init_window()

    def window_signals(self):
        """信号出发子线程启动"""
        self.Shp2dxf.process_btn.clicked.connect(lambda: self.shp2dxf_layering_thread(self.Shp2dxf.process))
        self.Shp2dxf_origin.shp2dxf_process_btn.clicked.connect(lambda: self.Shp2dxf_origin_layering_thread(self.Shp2dxf_origin.process))


        # 结束任务



    def loading_chart(self, widget):
        """加载图表"""
        # widget.chart_view.load(QUrl.fromLocalFile(os.path.abspath("lineChart.html")))  # 加载生成的图形
        widget.chart_view.setHtml(getattr(self.tool, 'html'))  # 加载生成的图形

    def shp2dxf_layering_thread(self, widget):
            """"""
            self.worker = Worker(widget)
            self.worker.finished.connect(self.showFlyout)
            self.worker.start()  # 启动任务
            self.worker.stop()
    def Shp2dxf_origin_layering_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务
        self.worker.stop()



    def showFlyout(self):
        # 结束时弹窗
        Flyout.make(CustomFlyoutView(), self.Shp2dxf.process_btn, self, aniType=FlyoutAnimationType.DROP_DOWN)

    def init_navigation(self):
        """添加UI"""
        self.addSubInterface(self.Shp2dxf_origin, FIF.APPLICATION, 'shp to dxf 保存全部字段')
        self.addSubInterface(self.Shp2dxf, FIF.PIE_SINGLE, 'shp to dxf 按字段保存为多个DXF文件')
        self.addSubInterface(
            self.Document, FIF.DOCUMENT, self.tr('简介'), NavigationItemPosition.BOTTOM)

    def click_prompt_signal(self):
        """提示信号"""
        self.tool.prompt(self.Shp2dxf.shp2dxf_prompt, Content.SHP2DXF_TITLE.value, Content.SHP2DXF_CONTENT.value)

        self.tool.prompt(self.Shp2dxf_origin.shp2dxf_origin_prompt, Content.SHP2DXF_ORIGIN_TITLE.value, Content.SHP2DXF_ORIGIN_CONTENT.value)
    def init_window(self):
        self.resize(1100, 800)
        self.setWindowIcon(QIcon(':/icons/images/icon.ico'))
        self.setWindowTitle('遥感数据处理工具')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
