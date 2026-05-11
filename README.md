# iOS 图片倍率处理工具

一款基于 PySide6 开发的跨平台桌面客户端工具，用于 iOS 图片倍率转换。

## 功能特性

- **倍率选择**：支持选择原图倍率（1x/2x/3x）
- **批量导入**：支持点击选择和拖拽导入图片
- **自动生成**：根据原图自动生成 1x、2x、3x 倍率图片
- **智能命名**：自动识别并规范化 iOS 图片命名规范
- **自定义输出**：支持选择输出目录，自动创建目录结构

## 技术栈

- Python 3.11+
- PySide6
- Pillow
- qfluentwidgets（可选）

## 项目结构

```
ios_image_tool/
├── main.py                 # 入口文件
├── requirements.txt        # 依赖配置
├── README.md              # 项目说明
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # 主窗口
│   ├── widgets/           # 自定义控件
│   │   ├── __init__.py
│   │   ├── scale_selector_widget.py   # 倍率选择器
│   │   ├── drop_zone_widget.py        # 拖拽上传区域
│   │   └── image_list_widget.py       # 图片列表
│   └── styles/            # 样式文件
│       ├── __init__.py
│       └── main_style.qss
├── services/              # 服务层
│   ├── __init__.py
│   ├── image_service.py   # 图片处理服务
│   └── file_service.py    # 文件服务
├── resources/             # 资源文件
│   ├── __init__.py
│   └── icons/
└── utils/                 # 工具类
    └── __init__.py
```

## 安装步骤

```bash
# 安装依赖
pip install -r requirements.txt
```

## 运行步骤

```bash
python main.py
```

## 使用说明

1. **选择原图倍率**：在顶部选择输入图片的倍率（1x/2x/3x）
2. **导入图片**：
   - 点击拖拽区域选择图片
   - 或直接拖拽图片到窗口中
3. **设置输出目录**：默认输出到桌面 `iOSImages` 目录
4. **开始转换**：点击「开始转换」按钮，自动生成所有倍率图片

## 图片转换规则

| 原图倍率 | 生成倍率 | 缩放比例 |
|---------|---------|---------|
| 1x | 1x, 2x, 3x | 1.0, 2.0, 3.0 |
| 2x | 1x, 2x, 3x | 0.5, 1.0, 1.5 |
| 3x | 1x, 2x, 3x | 1/3, 2/3, 1.0 |

## 输出目录结构

```
输出目录/
├── icon/
│   ├── icon.png
│   ├── icon@2x.png
│   └── icon@3x.png
├── logo/
│   ├── logo.png
│   ├── logo@2x.png
│   └── logo@3x.png
└── ...
```

## 打包步骤

### macOS

```bash
pyinstaller --onefile --windowed --name "iOSImageTool" --icon=resources/icons/app.icns main.py
```

### Windows

```bash
pyinstaller --onefile --windowed --name "iOSImageTool" --icon=resources/icons/app.ico main.py
```

## 支持的图片格式

- PNG
- JPG/JPEG
- WebP

## 预留扩展能力

- SVG 转换支持
- xcassets 自动生成
- Android drawable 支持

## 许可证

MIT License
