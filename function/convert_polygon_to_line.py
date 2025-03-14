from osgeo import ogr


def polygons_to_lines(input_shp, output_shp):
    """
    Convert a polygon shapefile to a line shapefile representing polygon boundaries.

    Parameters:
    input_shp (str): Path to the input polygon shapefile.
    output_shp (str): Path to the output line shapefile.
    """
    # 打开输入面矢量文件
    input_ds = ogr.Open(input_shp)
    if input_ds is None:
        raise Exception(f"无法打开输入文件: {input_shp}")
    input_layer = input_ds.GetLayer()

    # 创建输出线矢量文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if driver is None:
        raise Exception("ESRI Shapefile驱动不可用")
    output_ds = driver.CreateDataSource(output_shp)
    if output_ds is None:
        raise Exception(f"无法创建输出文件: {output_shp}")
    output_layer = output_ds.CreateLayer(
        "lines", geom_type=ogr.wkbLineString, srs=input_layer.GetSpatialRef()
    )

    # 复制属性表结构
    input_defn = input_layer.GetLayerDefn()
    for i in range(input_defn.GetFieldCount()):
        field_defn = input_defn.GetFieldDefn(i)
        output_layer.CreateField(field_defn)

    # 遍历面要素，提取边界线
    for feature in input_layer:
        geom = feature.GetGeometryRef()
        if geom is not None:
            boundary = geom.Boundary()  # 获取面的边界线
            if boundary is not None:
                # 处理单一线条（简单多边形无洞）
                if boundary.GetGeometryType() == ogr.wkbLineString:
                    out_feature = ogr.Feature(output_layer.GetLayerDefn())
                    out_feature.SetGeometry(boundary)
                    # 复制属性
                    for i in range(input_defn.GetFieldCount()):
                        out_feature.SetField(i, feature.GetField(i))
                    output_layer.CreateFeature(out_feature)
                    out_feature = None
                # 处理多线条（带洞的多边形或多多边形）
                elif boundary.GetGeometryType() == ogr.wkbMultiLineString:
                    for i in range(boundary.GetGeometryCount()):
                        line = boundary.GetGeometryRef(i)
                        out_feature = ogr.Feature(output_layer.GetLayerDefn())
                        out_feature.SetGeometry(line)
                        # 复制属性
                        for j in range(input_defn.GetFieldCount()):
                            out_feature.SetField(j, feature.GetField(j))
                        output_layer.CreateFeature(out_feature)
                        out_feature = None

    # 清理资源
    output_ds = None
    input_ds = None

if __name__ == "__main__":
    input_shp = r"E:\陆表赛题自然田型提取\训练\标签\zrtx-cx-label.shp"
    output_shp = r"E:\陆表赛题自然田型提取\训练\标签\zrtx-cx-label_lines.shp"
    polygons_to_lines(input_shp, output_shp)