
# RS Tool - 遥感数据处理工具

基于PyQt5开发的跨平台遥感数据处理工具，集成GDAL/OGR进行空间数据转换与分析。提供图形化界面操作，支持栅格影像处理与矢量数据格式转换。
## 项目介绍
RS Tool是一款开源的遥感数据处理工具，旨在简化遥感数据的处理与分析工作。通过集成GDAL/OGR库，提供了丰富的空间数据处理功能，包括栅格影像有效范围提取、矢量数据转换工具。
## 功能特性

### 已实现功能
- **栅格影像有效范围提取**  
  - 自动识别有效像素区域边界
  - 输出Shapefile格式矢量轮廓
  - 支持多波段影像处理

- **矢量数据转换工具**  
  - Shapefile面要素转线要素
  - 带进度显示的异步处理
  - 支持复杂多边形分解

- **无人机数据处理**
  - 照片GPS信息提取
  - 输出带坐标的Shapefile
  - 批量处理JPG/RAW格式

### 计划功能
- [ ] 矢量数据裁剪工具
- [ ] 坐标系批量转换
- [ ] 属性表字段计算器

## 技术架构
.
├── rstool.py                   # 主程序入口
├── resources/                  # 资源文件
│   ├── shpPolygon2Polyline.py  # 面转线核心实现
│   └──... 
├── ui/                         # 界面组件
│   ├── ui_polygon2polyline.py  # 面转线界面
│   └──... 
└── function/                   # 业务逻辑
    ├── tools.py                # 工具类 
    └──...


## 安装部署
```bash
# 安装依赖
pip install pyqt5 qfluentwidgets gdal pyinstaller

# 运行面转线工具
python shpPolygon2Polyline.py

# 打包独立可执行文件
pyinstaller --onefile --windowed --icon=.\resources\logo.ico rstool.py


## 更新日志
### v0.0.8 - 2025.03
- 新增矢量面转线核心功能 `Polygon2Polyline_process_btn`
- 优化多线程处理稳定性
- 修复中文路径支持问题
- 实现栅格轮廓生成基础功能
- 构建主界面框架 `Window`

## 注意事项
1. GDAL需要配置环境变量（Windows需安装对应版本）
2. 建议在非系统目录执行数据转换
3. 支持Windows 10/11及Ubuntu 20.04+系统
4. 处理大型数据时预留充足磁盘空间


0.0.9更新
- 新增遥感影像黑边去除处理功能
- 美化按钮布局

