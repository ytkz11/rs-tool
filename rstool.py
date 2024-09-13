# - coding:utf-8 -

"""备份new_run文件"""

from PyQt5.QtGui import QIcon
from qfluentwidgets import (FluentWindow, NavigationItemPosition, Flyout, FlyoutAnimationType)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from resources.Flyout_ import CustomFlyoutView
from function.messages import Content
from function.tools import Tool

from ui.ui_document import DocumentWidget
from ui.ui_thread import Worker
from ui.ui_shp2dxf import shp2dxfWidget
from ui.ui_shp2dxf_origin import shp2dxfWidget_origin
from ui.ui_shp2kml import shp2kmlWidget_origin
from ui.ui_color_enhance import color_enhanceWidget

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, SplitFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)


from qfluentwidgets import FluentIcon as FIF
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)
class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.tool = Tool()
        self.Color_enhance = color_enhanceWidget('color_enhanceWidget', self)

        self.Shp2dxf = shp2dxfWidget('shp2dxf_ui', self)
        self.Shp2dxf_origin = shp2dxfWidget_origin('shp2dxf_origin_ui', self)
        self.Shp2kml = shp2kmlWidget_origin('shp2kml_ui', self)

        self.Document = DocumentWidget("document_ui", self)
        self.homeInterface = Widget('Home Interface', self)
        self.gridInterface = Widget('栅格页面，未完成，添加1个功能', self)
        self.vectorInterface = Widget('矢量页面，未完成，添加3个功能', self)
        self.droneInterface = Widget('无人机处理专题页面，未完成，未添加功能，待完善', self)


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
        self.Color_enhance.color_process_btn.clicked.connect(lambda: self.color_enhance_thread(self.Color_enhance.process))
        self.Shp2dxf.process_btn.clicked.connect(lambda: self.shp2dxf_layering_thread(self.Shp2dxf.process))
        self.Shp2dxf_origin.shp2dxf_process_btn.clicked.connect(lambda: self.Shp2dxf_origin_layering_thread(self.Shp2dxf_origin.process))
        self.Shp2kml.shp2kml_process_btn.clicked.connect(lambda: self.Shp2kml_thread(self.Shp2kml.process))
    def color_enhance_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务

    def shp2dxf_layering_thread(self, widget):
            """"""
            self.worker = Worker(widget)
            self.worker.finished.connect(self.showFlyout)
            self.worker.start()  # 启动任务

    def Shp2dxf_origin_layering_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务

    def Shp2kml_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务



    def showFlyout(self):
        # 结束时弹窗
        Flyout.make(CustomFlyoutView(), self.Shp2dxf.process_btn, self, aniType=FlyoutAnimationType.DROP_DOWN)

    def init_navigation(self):
        """添加UI"""

        self.addSubInterface(self.gridInterface, FIF.VIDEO, '栅格', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.vectorInterface, FIF.TILES, '矢量', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.droneInterface, FIF.ALBUM, '无人机', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Color_enhance, FIF.LEAF, '植被色彩增强', parent=self.gridInterface)

        self.addSubInterface(self.Shp2dxf_origin, FIF.APPLICATION, 'shp to dxf 保存全部字段', parent=self.vectorInterface)
        self.addSubInterface(self.Shp2dxf, FIF.PIE_SINGLE, 'shp to dxf 按字段保存为多个DXF文件',parent=self.vectorInterface)
        self.addSubInterface(self.Shp2kml, FIF.PIN, 'shp to kml',parent=self.vectorInterface)



        self.addSubInterface(
            self.Document, FIF.DOCUMENT, self.tr('简介'), NavigationItemPosition.BOTTOM)

    def click_prompt_signal(self):
        """提示信号"""
        self.tool.prompt(self.Color_enhance.colorenhance_prompt, Content.ColorEnhancement_TITLE.value, Content.ColorEnhancement_CONTENT.value)
        self.tool.prompt(self.Shp2dxf.shp2dxf_prompt, Content.SHP2DXF_TITLE.value, Content.SHP2DXF_CONTENT.value)
        self.tool.prompt(self.Shp2dxf_origin.shp2dxf_origin_prompt, Content.SHP2DXF_ORIGIN_TITLE.value, Content.SHP2DXF_ORIGIN_CONTENT.value)
        self.tool.prompt(self.Shp2kml.shp2kml_prompt, Content.SHP2KML_TITLE.value, Content.SHP2KML_CONTENT.value)

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
    # pyinstaller -F -w -i G:\code\rstool\resources\images\icon.ico rstool.py