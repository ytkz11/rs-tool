import os.path
from osgeo import ogr

ogr.UseExceptions()  # 启用异常处理
class Shp_split:
    def __init__(self, filename):
        self.filename = filename
        self.driver = ogr.GetDriverByName('ESRI Shapefile')
        self.datasource = self.driver.Open(filename, 0)  # 0 means read-only
        self.get_field_name()
        self.layer = self.datasource.GetLayer()
    def get_field_name(self):
        ds = self.datasource
        layer = ds.GetLayer()
        layer_defn = layer.GetLayerDefn()
        field_contents = []
        # 遍历所有的字段
        for i in range(layer_defn.GetFieldCount()):
            fieldDefn = layer_defn.GetFieldDefn(i)
            field_contents.append(fieldDefn.GetName())
        self.field = field_contents
        # 关闭数据源
        ds = None

        self.field_contents = field_contents
    def get_unique_values(self, field_name):

        # 获取字段定义
        layerDefn = self.layer.GetLayerDefn()
        fieldIndex = layerDefn.GetFieldIndex(field_name)

        # 检查字段是否存在
        if fieldIndex == -1:
            print("Field not found.")
        else:
            # 获取所有记录
            values = []
            for feature in self.layer:
                value = feature.GetFieldAsString(fieldIndex)
                if value is not None:
                    values.append(value)

            return values

    def split_by_field(self, field_name, value):

            # 打开输入的 Shapefile 数据源

            data_source = self.datasource
            if data_source is None:
                print(f'Could not open {self.filename}')
                return

            # 获取数据源中的第一层（通常一个 Shapefile 只有一层）
            layer = data_source.GetLayer()
            if layer is None:
                print(f'No layer found in {self.filename}')
                return

            output_shp_file = os.path.splitext(os.path.basename(self.filename))[0] +'_'+ field_name + '_' +value +'.shp'
            outpath = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "out")
            os.makedirs(outpath, exist_ok=True)

            output_shp = os.path.join(outpath, output_shp_file)
            # 创建输出的 Shapefile 数据源
            # if ogr.GetDriverByName('ESRI Shapefile').Exists(output_shp):
            #     ogr.GetDriverByName('ESRI Shapefile').DeleteDataSource(output_shp)
            out_data_source = self.driver.CreateDataSource(output_shp)
            if out_data_source is None:
                print(f'Could not create {output_shp}')
                return

            # 复制输入层的定义以创建输出层
            out_layer = out_data_source.CreateLayer(output_shp.split('.')[0], geom_type=layer.GetGeomType())
            for i in range(layer.GetLayerDefn().GetFieldCount()):
                field_defn = layer.GetLayerDefn().GetFieldDefn(i)
                out_layer.CreateField(field_defn)

            # 设置过滤器
            layer.SetAttributeFilter(f"{field_name} = '{value}'")

            # 遍历并复制匹配的特征
            feature = layer.GetNextFeature()
            while feature:
                out_feature = ogr.Feature(out_layer.GetLayerDefn())
                out_feature.SetFrom(feature)
                out_layer.CreateFeature(out_feature)
                out_feature = None  # 释放内存
                feature = layer.GetNextFeature()

            # 关闭数据源
            data_source = None
            out_data_source = None

if __name__ == '__main__':
    file_path = r'D:\code\arcgis-online-download\utils\layers\services7.arcgis.com\iEMmryaM5E3wkdnU\China_Provinces_1389.shp'
    splitter = Shp_split(file_path)
    field_name = 'LABEL_CHN'  # Replace with the actual field name you want to use
    splitter.split_by_field(field_name)