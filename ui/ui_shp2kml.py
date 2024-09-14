#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_shp2dxf.py
# time: 2024/9/7 16:12
# 不按属性分层，输出全部图形
import os
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from function.tools import Tool
from resources.shpkml import Ui_Form
from PyQt5.QtWidgets import QFrame
from function.shp2kml_with_label import convert_to_kml
from function.transfer_project import transform_coordinate_and_recreate_new_dbf

from osgeo import ogr

class shp2kmlWidget_origin(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(shp2kmlWidget_origin, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()

    def signals(self):
        """按钮触发， 主动调用"""
        self.shp2kml_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.shp2kml_filepath_line))
        self.shp2kml_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.shp2kml_filepath_line)
        if self.tool.suffix not in ['.shp']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.shp2kml_process_btn.setEnabled(True)
        else:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.shp2kml_process_btn.setEnabled(False)
    def process(self):
        """处理"""

        if self.tool.path:
            if self.tool.suffix == ".shp":
                if os.path.exists(self.tool.path):
                    self.progressBar.start()



                    # 检查坐标系统是否为 WGS84
                    if check_is_84(self.tool.path):
                        print(f'The projection of the file is WGS84.')
                        convert_to_kml(self.tool.path)
                        self.progressBar.stop()
                    else:
                        print(f'The projection of the file is not WGS84.')
                        tempshp_file_name = transform_coordinate_and_recreate_new_dbf(self.tool.path, os.path.dirname(self.tool.path))
                        convert_to_kml(tempshp_file_name, self.tool.path)
                        print("删除中间文件")
                        try :
                            # for file in [utf8_file, tempshp_file_name]:
                            for file in [tempshp_file_name]:
                                for suf in ['.shp', '.shx', '.dbf', '.proj']:
                                    os.remove(os.path.splitext(file)[0]+suf)
                        except Exception as e:
                            print(e)

                        '''
                            VectorTranslate(
        shapeFilePath,
        saveFolderPath,
        format="ESRI Shapefile",
        accessMode=None,
        dstSrsESPG=4326,
        selectFields=None,
        geometryType="POLYGON",
        dim="XY",
    )
                        '''

                else:
                    self.shp2kml_process_btn.setText("请输入正确的shp文件路径，再点击")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")
            else:
                self.tool.show_error(self, "❗️文件错误", "文件后缀错误")

def check_is_84(file):
    ds = ogr.Open(file)
    layer = ds.GetLayer()
    spatial_ref = layer.GetSpatialRef()

    wkt = spatial_ref.ExportToPrettyWkt()

    if 'WGS_1984' in wkt:
        return True
    else:
        return False
