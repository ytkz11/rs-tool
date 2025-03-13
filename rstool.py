# - coding:utf-8 -

"""备份new_run文件"""

from PyQt5.QtGui import QIcon
from qfluentwidgets import (FluentWindow, Flyout, FlyoutAnimationType)
from resources.Flyout_ import CustomFlyoutView
from function.messages import Content
from function.tools import Tool

from ui.ui_color_enhance import color_enhanceWidget
from ui.ui_imagefootprint import imagefootprintWidget

from ui.ui_document import DocumentWidget
from ui.ui_thread import Worker
from ui.ui_shp2dxf import shp2dxfWidget
from ui.ui_shp2dxf_origin import shp2dxfWidget_origin
from ui.ui_polygon2polyline import polygon2polylineWidget
from ui.ui_shp2kml import shp2kmlWidget_origin


from ui.ui_restoreshp import restore_shpWidget
from ui.ui_photo_extrat_gps_shp import photo_extrat_gps_shpWidget
from ui.ui_shpsplit import shpsplitWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (
    NavigationItemPosition, MessageBox, setTheme, Theme, SplitFluentWindow,
    NavigationAvatarWidget, qrouter, SubtitleLabel, setFont,
    PrimaryPushButton  # 添加缺失的组件导入
)

from qfluentwidgets import FluentIcon as FIF
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        # self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        # setFont(self.label, 24)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))
        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 12, 0, 0)
class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.tool = Tool()
        self.Color_enhance = color_enhanceWidget('color_enhanceWidget', self)
        
        self.Image_footprint = imagefootprintWidget('image_footprintWidget', self)
        self.Restore_shp = restore_shpWidget('restore_shpWidget', self)
        self.Photo_extrat_gps_shp = photo_extrat_gps_shpWidget('photo_extrat_gps_shpWidget', self)


        self.Shp2dxf = shp2dxfWidget('shp2dxf_ui', self)
        self.Shp2dxf_origin = shp2dxfWidget_origin('shp2dxf_origin_ui', self)
        self.Polygon2Polyline = polygon2polylineWidget('polygon2polyline_ui', self)
        self.Shpsplit =shpsplitWidget('shpsplit_ui', self)
        self.Shp2kml = shp2kmlWidget_origin('shp2kml_ui', self)

        self.Document = DocumentWidget("document_ui", self)
        self.homeInterface = Widget('home', self)
        self.vectorInterface = Widget('1', self)
        # self.droneInterface = Widget(' ', self)
        # 修改栅格页面初始化
        self.gridInterface = Widget('栅格',self)
        self.init_grid_interface()  # 新增初始化方法
        self.init_vector_interface()

    def init_grid_interface(self):
        """初始化栅格页面布局"""
        # 创建水平布局存放按钮
        button_layout = QHBoxLayout()

        # # 植被色彩增强按钮
        self.color_btn = PrimaryPushButton('植被色彩增强', self.gridInterface)
        # self.color_btn.setIcon(FIF.LEAF)
        # # 修改导航参数：第一个参数改为窗口实例 self
        # self.color_btn.clicked.connect(lambda: qrouter.push(self, self.Color_enhance))

        # # 影像有效范围按钮
        self.footprint_btn = PrimaryPushButton('影像有效范围', self.gridInterface)

        # 植被色彩增强按钮导航
        self.color_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Color_enhance))
        # 影像有效范围按钮导航
        self.footprint_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Image_footprint))
                # 将按钮添加到布局
        button_layout.addWidget(self.color_btn)
        button_layout.addWidget(self.footprint_btn)

        # 将按钮布局添加到主布局
        self.gridInterface.hBoxLayout.addLayout(button_layout)
        """初始化界面"""
        self.success_fired = False
        self.warn_fired = False
        self.error_fired = False
        self.init_navigation()
        # self.add_loading_ui()
        self.click_prompt_signal()
        self.window_signals()
        self.init_window()
    def init_vector_interface(self):
        """初始化矢量页面布局"""
        # 创建水平布局存放按钮
        button_layout = QHBoxLayout()
        # # 矢量转栅格按钮
        self.Polygon2Polyline_btn = PrimaryPushButton('矢量转线', self.vectorInterface)
        self.Polygon2Polyline_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Polygon2Polyline))
        self.Shp2dxf_btn = PrimaryPushButton('矢量分层', self.vectorInterface)
        self.Shp2dxf_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Shp2dxf))
        self.Shp2dxf_origin_btn = PrimaryPushButton('矢量分层(不按属性分层)', self.vectorInterface)
        self.Shp2dxf_origin_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Shp2dxf_origin))
        self.Shpsplit_btn = PrimaryPushButton('矢量拆分', self.vectorInterface)
        self.Shpsplit_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Shpsplit))
        self.Shp2kml_btn = PrimaryPushButton('矢量转kml', self.vectorInterface)
        self.Shp2kml_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Shp2kml))
        self.Restore_shp_btn = PrimaryPushButton('矢量修复', self.vectorInterface)
        self.Restore_shp_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Restore_shp))
        self.Photo_extrat_gps_shp_btn = PrimaryPushButton('从图片提取GPS信息', self.vectorInterface)
        self.Photo_extrat_gps_shp_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Photo_extrat_gps_shp))

        # 将按钮添加到布局
        # button_layout.addWidget(self.footprint_btn)
        button_layout.addWidget(self.Polygon2Polyline_btn)
        button_layout.addWidget(self.Shp2dxf_btn)
        button_layout.addWidget(self.Shp2dxf_origin_btn)
        button_layout.addWidget(self.Shpsplit_btn)
        button_layout.addWidget(self.Shp2kml_btn)
        button_layout.addWidget(self.Restore_shp_btn)


        # 将按钮布局添加到主布局
        self.vectorInterface.hBoxLayout.addLayout(button_layout)

        """初始化界面"""
        self.success_fired = False
        self.warn_fired = False

    def window_signals(self):
        """信号出发子线程启动"""
        self.Color_enhance.color_process_btn.clicked.connect(lambda: self.color_enhance_thread(self.Color_enhance.process))
        self.Image_footprint.imagefootprint_process_btn.clicked.connect(lambda: self.Image_footprint.process())
        self.Shp2dxf.process_btn.clicked.connect(lambda: self.shp2dxf_layering_thread(self.Shp2dxf.process))
        self.Shp2dxf_origin.shp2dxf_process_btn.clicked.connect(lambda: self.Shp2dxf_origin_layering_thread(self.Shp2dxf_origin.process))
        self.Polygon2Polyline.Polygon2Polyline_process_btn.clicked.connect(lambda: self.Polygon2Polyline_thread(self.Polygon2Polyline.process))
        self.Shpsplit.process_btn.clicked.connect(lambda: self.Shp_split_thread(self.Shpsplit.process))
        self.Shp2kml.shp2kml_process_btn.clicked.connect(lambda: self.Shp2kml_thread(self.Shp2kml.process))
        self.Restore_shp.restoreshp_process_btn.clicked.connect(lambda: self.restore_shp_thread(self.Restore_shp.process))
        self.Photo_extrat_gps_shp.photo_to_gps_shp_process_btn.clicked.connect(lambda: self.Photo_extrat_gps_shp_thread(self.Photo_extrat_gps_shp.process))

    def Shp_split_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务
    def Photo_extrat_gps_shp_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务
    def restore_shp_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务

    def color_enhance_thread(self,widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()  # 启动任务
    def Image_footprint_thread(self,widget):
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
    def Polygon2Polyline_thread(self,widget):
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
        # self.addSubInterface(self.droneInterface, FIF.ALBUM, '无人机', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Color_enhance, FIF.LEAF, '植被色彩增强', parent=self.gridInterface)
        self.addSubInterface(self.Image_footprint, FIF.SCROLL, '影像有效范围', parent=self.gridInterface)
        self.addSubInterface(self.Shp2dxf_origin, FIF.APPLICATION, 'shp to dxf 保存全部字段', parent=self.vectorInterface)
        self.addSubInterface(self.Polygon2Polyline, FIF.PIE_SINGLE, '面矢量转换线矢量', parent=self.vectorInterface)
        self.addSubInterface(self.Shp2dxf, FIF.PIE_SINGLE, 'shp to dxf 按字段保存为多个DXF文件',parent=self.vectorInterface)
        self.addSubInterface(self.Shpsplit, FIF.PIE_SINGLE, 'shp按字段保存',parent=self.vectorInterface)

        self.addSubInterface(self.Shp2kml, FIF.PIN, 'shp to kml',parent=self.vectorInterface)
        self.addSubInterface(self.Restore_shp, FIF.UPDATE, 'shp修复', parent=self.vectorInterface)
        self.addSubInterface(self.Photo_extrat_gps_shp, FIF.UPDATE, '照片提取GPS', parent=self.vectorInterface)

        self.addSubInterface(
            self.Document, FIF.DOCUMENT, self.tr('简介'), NavigationItemPosition.BOTTOM)

    def click_prompt_signal(self):
        """提示信号"""
        self.tool.prompt(self.Color_enhance.colorenhance_prompt, Content.ColorEnhancement_TITLE.value, Content.ColorEnhancement_CONTENT.value)
        self.tool.prompt(self.Image_footprint.imagefootprint_prompt, Content.IMAGEFOOTPRINT_TITLE.value, Content.IMAGEFOOTPRINT_CONTENT.value)
        self.tool.prompt(self.Shp2dxf.shp2dxf_prompt, Content.SHP2DXF_TITLE.value, Content.SHP2DXF_CONTENT.value)
        self.tool.prompt(self.Shp2dxf_origin.shp2dxf_origin_prompt, Content.SHP2DXF_ORIGIN_TITLE.value, Content.SHP2DXF_ORIGIN_CONTENT.value)
        self.tool.prompt(self.Polygon2Polyline.Polygon2Polyline_prompt, Content.POLYGON2POLYLINE_TITLE.value, Content.POLYGON2POLYLINE_CONTENT.value)
        # self.tool.prompt(self.Shpsplit.shpsplit_prompt, Content.SHPSPLIT_TITLE.value, Content.SHPSPLIT_CONTENT.value)

        self.tool.prompt(self.Shp2kml.shp2kml_prompt, Content.SHP2KML_TITLE.value, Content.SHP2KML_CONTENT.value)
        self.tool.prompt(self.Restore_shp.restoreshp_prompt, Content.RESTORESHP_TITLE.value, Content.RESTORESHP_CONTENT.value)
        self.tool.prompt(self.Photo_extrat_gps_shp.photo_to_gps_shp_prompt, Content.PHOTOGPS_TITLE.value, Content.PHOTOGPS_CONTENT.value)

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
    # pyinstaller -F -w -i D:\code\rstool\resources\images\icon.ico rstool.py
    # pyinstaller -F -w -i G:\code\rstool\resources\images\icon.ico rstool.py