from osgeo import ogr
import os
from shp2dxf_ezdxf_padding import Shp2DxfPadding

from osgeo import ogr

ogr.UseExceptions()  # 启用异常处理
class Shp_split:
    def __init__(self, filename):
        self.filename = filename
        self.driver = ogr.GetDriverByName('ESRI Shapefile')
        self.datasource = self.driver.Open(filename, 0)  # 0 means read-only
        self.layer = self.datasource.GetLayer()

    def get_unique_values(self, field_name):
        unique_values = set()
        feature_defn = self.layer.GetLayerDefn()
        for feature in self.layer:
            if feature_defn.GetFieldIndex(field_name) >= 0:
                value = feature.GetField(field_name)
                if value is not None:
                    unique_values.add(value)
        return list(unique_values)

    def split_by_field(self, field_name):
        unique_values = self.get_unique_values(field_name)
        for value in unique_values:
            output_filename = f"{self.filename[:-4]}_{value}.shp"
            out_datasource = self.driver.CreateDataSource(output_filename)
            out_layer = out_datasource.CreateLayer(output_filename, geom_type=self.layer.GetGeomType())

            # Copy all the original layer's attributes to the new layer
            in_layer_defn = self.layer.GetLayerDefn()
            for i in range(in_layer_defn.GetFieldCount()):
                field_defn = in_layer_defn.GetFieldDefn(i)
                out_layer.CreateField(field_defn)

            # Feature definition for the output layer
            out_layer_defn = out_layer.GetLayerDefn()

            query = f"{field_name} = '{value}'"
            self.layer.SetAttributeFilter(query)
            for feature in self.layer:
                out_feature = ogr.Feature(out_layer_defn)
                out_feature.SetGeometry(feature.GetGeometryRef())
                for i in range(out_layer_defn.GetFieldCount()):
                    out_feature.SetField(out_layer_defn.GetFieldDefn(i).GetNameRef(), feature.GetField(i))
                out_layer.CreateFeature(out_feature)
                out_feature = None  # destroy feature to free memory

            self.layer.SetAttributeFilter(None)  # reset filter
            out_datasource = None  # close output datasource




if __name__ == '__main__':
    file_path = r'D:\code\arcgis-online-download\utils\layers\services7.arcgis.com\iEMmryaM5E3wkdnU\China_Provinces_1389.shp'
    file_path =r'D:\BaiduNetdiskDownload\新建文件夹\photos.shp'
    splitter = Shp_split(file_path)
    field_name = 'LABEL_CHN'  # Replace with the actual field name you want to use
    splitter.split_by_field(field_name)