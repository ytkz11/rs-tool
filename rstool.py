# - coding:utf-8 -

"""Remote Sensing Data Processing Tool"""

from qfluentwidgets import NavigationItemPosition,FluentWindow, Flyout, FlyoutAnimationType, FlowLayout, SubtitleLabel, PrimaryPushButton, setTheme, Theme, FluentIcon as FIF
from qfluentwidgets import FluentIcon as FIF
from resources.Flyout_ import CustomFlyoutView
from function.messages import Content
from function.tools import Tool
from ui.ui_color_enhance import color_enhanceWidget
from ui.ui_remove_black_edge import RemoveBlackEdgeWidget
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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout

class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QVBoxLayout(self)
        self.setObjectName(text.replace(' ', '-'))
        self.hBoxLayout.setContentsMargins(0, 12, 0, 0)

class Window(FluentWindow):
    """Main Interface"""

    def __init__(self):
        super().__init__()
        self.tool = Tool()
        self.Color_enhance = color_enhanceWidget('color_enhanceWidget', self)
        self.Remove_black_edge = RemoveBlackEdgeWidget('remove_black_edgeWidget', self)
        self.Image_footprint = imagefootprintWidget('image_footprintWidget', self)
        self.Restore_shp = restore_shpWidget('restore_shpWidget', self)
        self.Photo_extrat_gps_shp = photo_extrat_gps_shpWidget('photo_extrat_gps_shpWidget', self)
        self.Shp2dxf = shp2dxfWidget('shp2dxf_ui', self)
        self.Shp2dxf_origin = shp2dxfWidget_origin('shp2dxf_origin_ui', self)
        self.Polygon2Polyline = polygon2polylineWidget('polygon2polyline_ui', self)
        self.Shpsplit = shpsplitWidget('shpsplit_ui', self)
        self.Shp2kml = shp2kmlWidget_origin('shp2kml_ui', self)
        self.Document = DocumentWidget("document_ui", self)
        self.homeInterface = Widget('home', self)
        self.vectorInterface = Widget('vector', self)
        self.gridInterface = Widget('grid', self)
        self.init_navigation()
        self.click_prompt_signal()
        self.window_signals()
        self.init_window()
        self.init_grid_interface()
        self.init_vector_interface()

    def init_grid_interface(self):
        """Initialize the grid interface layout with beautified button arrangement"""
        setTheme(Theme.LIGHT)

        main_layout = QVBoxLayout(self.gridInterface)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        button_layout = FlowLayout()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 10, 0, 10)
        grid_buttons = [
            ( "植被色彩增强", self.Color_enhance),
            ( "影像有效范围", self.Image_footprint),
            ( "去除影像黑边", self.Remove_black_edge),
        ]
        button_width = 200  # Match vector interface button width
        button_style = """
            PrimaryPushButton {
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            PrimaryPushButton:hover {
                background-color: #40C4FF;
                color: white;
            }
        """
        for title, widget in grid_buttons:
            btn = PrimaryPushButton(title, self.gridInterface)
            btn.setFixedWidth(button_width)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, w=widget: self.stackedWidget.setCurrentWidget(w))
            button_layout.addWidget(btn)



        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.success_fired = False
        self.warn_fired = False
        self.error_fired = False


    def init_vector_interface(self):
        """Initialize the vector interface layout with beautified button arrangement"""
        setTheme(Theme.LIGHT)
        main_layout = QVBoxLayout(self.vectorInterface)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)


        button_layout = FlowLayout()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 10, 0, 10)

        # 配置所有按钮
        vector_buttons = [
            ( "从图片提取GPS信息", self.Photo_extrat_gps_shp),
            ( "shp to dxf 保存全部字段", self.Shp2dxf_origin),
            ( "面矢量转换线矢量", self.Polygon2Polyline),
            ( "shp to dxf 按字段保存为多个DXF文件", self.Shp2dxf),
            ( "shp按字段保存", self.Shpsplit),
            ( "shp to kml", self.Shp2kml),
            ( "shp修复", self.Restore_shp)
        ]
        button_width = 200
        button_style = """
            PrimaryPushButton {
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            PrimaryPushButton:hover {
                background-color: #40C4FF;
                color: white;
            }
        """

        for title, widget in vector_buttons:
            btn = PrimaryPushButton(title, self.vectorInterface)
            btn.setFixedWidth(button_width)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, w=widget: self.stackedWidget.setCurrentWidget(w))
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

    def window_signals(self):
        """Connect signals to start threads"""
        self.Color_enhance.color_process_btn.clicked.connect(lambda: self.color_enhance_thread(self.Color_enhance.process))
        self.Remove_black_edge.process_btn.clicked.connect(lambda: self.remove_black_edge_thread(self.Remove_black_edge.process))
        self.Image_footprint.imagefootprint_process_btn.clicked.connect(lambda: self.Image_footprint.process())
        self.Shp2dxf.process_btn.clicked.connect(lambda: self.shp2dxf_layering_thread(self.Shp2dxf.process))
        self.Shp2dxf_origin.shp2dxf_process_btn.clicked.connect(lambda: self.Shp2dxf_origin_layering_thread(self.Shp2dxf_origin.process))
        self.Polygon2Polyline.Polygon2Polyline_process_btn.clicked.connect(lambda: self.Polygon2Polyline_thread(self.Polygon2Polyline.process))
        self.Shpsplit.process_btn.clicked.connect(lambda: self.Shp_split_thread(self.Shpsplit.process))
        self.Shp2kml.shp2kml_process_btn.clicked.connect(lambda: self.Shp2kml_thread(self.Shp2kml.process))
        self.Restore_shp.restoreshp_process_btn.clicked.connect(lambda: self.restore_shp_thread(self.Restore_shp.process))
        self.Photo_extrat_gps_shp.photo_to_gps_shp_process_btn.clicked.connect(lambda: self.Photo_extrat_gps_shp_thread(self.Photo_extrat_gps_shp.process))

    def Shp_split_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def Photo_extrat_gps_shp_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def restore_shp_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def color_enhance_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def remove_black_edge_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def Image_footprint_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def shp2dxf_layering_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def Shp2dxf_origin_layering_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def Polygon2Polyline_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def Shp2kml_thread(self, widget):
        self.worker = Worker(widget)
        self.worker.finished.connect(self.showFlyout)
        self.worker.start()

    def showFlyout(self):
        Flyout.make(CustomFlyoutView(), self.Shp2dxf.process_btn, self, aniType=FlyoutAnimationType.DROP_DOWN)

    def init_navigation(self):
        """添加UI"""

        # 栅格相关
        self.addSubInterface(self.gridInterface, FIF.PHOTO, '栅格', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Color_enhance, FIF.BRUSH, '植被色彩增强', parent=self.gridInterface)

        self.addSubInterface(self.gridInterface, FIF.VIDEO, '栅格', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.vectorInterface, FIF.TILES, '矢量', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Color_enhance, FIF.LEAF, '植被色彩增强', parent=self.gridInterface)
        self.addSubInterface(self.Image_footprint, FIF.SCROLL, '影像有效范围', parent=self.gridInterface)
        self.addSubInterface(self.Remove_black_edge, FIF.PIE_SINGLE, '去除影像黑边', parent=self.gridInterface)
        self.addSubInterface(self.Shp2dxf_origin, FIF.APPLICATION, 'shp to dxf 保存全部字段',
                             parent=self.vectorInterface)
        self.addSubInterface(self.Polygon2Polyline, FIF.PIE_SINGLE, '面矢量转换线矢量', parent=self.vectorInterface)
        self.addSubInterface(self.Shp2dxf, FIF.PIE_SINGLE, 'shp to dxf 按字段保存为多个DXF文件',
                             parent=self.vectorInterface)
        self.addSubInterface(self.Shpsplit, FIF.PIE_SINGLE, 'shp按字段保存', parent=self.vectorInterface)

        self.addSubInterface(self.Shp2kml, FIF.PIN, 'shp to kml', parent=self.vectorInterface)
        self.addSubInterface(self.Restore_shp, FIF.UPDATE, 'shp修复', parent=self.vectorInterface)
        self.addSubInterface(self.Photo_extrat_gps_shp, FIF.UPDATE, '照片提取GPS', parent=self.vectorInterface)

        self.addSubInterface(
            self.Document, FIF.DOCUMENT, self.tr('简介'), NavigationItemPosition.BOTTOM)

    def click_prompt_signal(self):
        """Prompt signals"""
        self.tool.prompt(self.Color_enhance.colorenhance_prompt, Content.ColorEnhancement_TITLE.value, Content.ColorEnhancement_CONTENT.value)
        self.tool.prompt(self.Image_footprint.imagefootprint_prompt, Content.IMAGEFOOTPRINT_TITLE.value, Content.IMAGEFOOTPRINT_CONTENT.value)
        self.tool.prompt(self.Shp2dxf.shp2dxf_prompt, Content.SHP2DXF_TITLE.value, Content.SHP2DXF_CONTENT.value)
        self.tool.prompt(self.Shp2dxf_origin.shp2dxf_origin_prompt, Content.SHP2DXF_ORIGIN_TITLE.value, Content.SHP2DXF_ORIGIN_CONTENT.value)
        self.tool.prompt(self.Polygon2Polyline.Polygon2Polyline_prompt, Content.POLYGON2POLYLINE_TITLE.value, Content.POLYGON2POLYLINE_CONTENT.value)
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