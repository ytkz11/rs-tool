#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/9/13 16:08 
# @File : check_is_84.py 
'''

'''

from osgeo import ogr

def check_is_84(file):
    ds = ogr.Open(file)
    layer = ds.GetLayer()
    spatial_ref = layer.GetSpatialRef()

    wkt = spatial_ref.ExportToPrettyWkt()

    if 'WGS_1984' in wkt:
        return True
    else:
        return False

if __name__ == '__main__':
    file = r'D:\temp\out\84\Fisheries_test_clip\Fisheries_test_clip.shp'
    check_is_84(file)
    print()
