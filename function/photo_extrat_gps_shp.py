# 从照片提取gps信息，然后保存为shp
import glob
import os
try:
   import Image
   import ImageDraw
except:
   from PIL import Image
   from PIL.ExifTags import TAGS
import shapefile


def exif(img):
   """
  从图片中返回EXIF元数据
  """
   exif_data = {}

   try:
       i = Image.open(img)  # 使用PIL库打开图片
       tags = i._getexif()  # 获取图片的EXIF标签

       for tag, value in tags.items():
           decoded = TAGS.get(tag, tag)  # 尝试从预定义的TAGS字典中获取标签的中文描述，否则使用标签ID
           exif_data[decoded] = value  # 将标签及其值存储到exif_data字典中

   except:
       pass  # 捕获所有异常并忽略，这通常不是一个好的做法，应该明确指定要捕获的异常

   return exif_data


def dms2dd(d, m, s, i):
   """
  将度/分/秒转换为十进制度
  """
   sec = float((m * 60) + s)  # 将分和秒转换为秒
   dec = float(sec / 3600)  # 将秒转换为小数度
   deg = float(d + dec)  # 将度和小数度相加

   if i.upper() == 'W':  # 如果方向是西
       deg = deg * -1  # 将度数变为负数

   elif i.upper() == 'S':  # 如果方向是南
       deg = deg * -1  # 将度数变为负数

   return float(deg)


def gps(exif):
   """
  从EXIF元数据中提取GPS信息
  """
   lat = None  # 纬度
   lon = None  # 经度

   if exif.get('GPSInfo'):  # 如果EXIF中包含GPS信息
       # 纬度
       coords = exif['GPSInfo']
       i = coords[1]  # 纬度方向（N/S）
       d = coords[2][0]  # 纬度度数
       m = coords[2][1]  # 纬度分钟
       s = coords[2][2]  # 纬度秒
       lat = dms2dd(d, m, s, i)  # 将纬度转换为十进制度

       # 经度
       i = coords[3]  # 经度方向（E/W）
       d = coords[4][0]  # 经度度数
       m = coords[4][1]  # 经度分钟
       s = coords[4][2]  # 经度秒
       lon = dms2dd(d, m, s, i)  # 将经度转换为十进制度

   return lat, lon

def photo_extract_gps_info_to_shp(photos,photo_dir):
    # 查找指定目录下的所有JPG照片
    # files = glob.glob(os.path.join(photo_dir, "*.jpg"))
    jpgfiles = glob.glob(os.path.join(photo_dir, "*.jpg"))
    pngfiles = glob.glob(os.path.join(photo_dir, "*.png"))

    files = jpgfiles + pngfiles
    # 从文件中提取GPS元数据
    for f in files:
        try:
            e = exif(f)
            lat, lon = gps(e)
            if lat is None or lon is None:
                continue
            else:
                photos[f] = [lon, lat]  # 注意：这里通常经度在前，纬度在后
        except Exception as e:
            print(e)

    # 构建一个包含照片文件名作为属性的点shapefile
    os.chdir(photo_dir)
    with shapefile.Writer("photos", shapefile.POINT) as w:
        w.field("NAME", "C", 80)  # 创建一个名为NAME的字符型字段，最大长度为80

        for f, coords in photos.items():
            w.point(*coords)  # 使用经度和纬度（注意顺序）创建一个点要素
            w.record(f)  # 为点要素添加文件名属性

    with open('photos.txt', 'w') as f:
        for _, coords in photos.items():
            print(coords[0])
            f.write(str(coords[0]))
            f.write(' ')
            f.write(str(coords[1]))
            f.write('\n')
    with open('photos.prj', 'w') as f:
        f.write("""GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]
    """)



if __name__ == '__main__':
   # 存储照片文件名和GPS坐标的字典
   photos = {}
   photo_dir = r"D:\无人机"
   photo_extract_gps_info_to_shp(photos,photo_dir)
