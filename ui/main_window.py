from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QProgressBar, QFileDialog,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices

from ui.widgets.scale_selector_widget import ScaleSelectorWidget
from ui.widgets.drop_zone_widget import DropZoneWidget
from ui.widgets.image_list_widget import ImageListWidget
from services.image_service import ImageService
from services.file_service import FileService

class WorkerThread(QThread):
    progress_updated = Signal(int)
    task_completed = Signal(bool, str)
    
    def __init__(self, items, output_dir, parent=None):
        super().__init__(parent)
        self.items = items
        self.output_dir = output_dir
    
    def run(self):
        total = len(self.items)
        completed = 0
        
        for item in self.items:
            success, result = ImageService.generate_scaled_images(
                item['file_path'],
                item['scale'],
                self.output_dir
            )
            
            if not success:
                self.task_completed.emit(False, result)
                return
            
            completed += 1
            progress = int((completed / total) * 100)
            self.progress_updated.emit(progress)
        
        self.task_completed.emit(True, "转换完成")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iOS 图片倍率处理工具")
        self.setWindowIcon(QIcon.fromTheme("image"))
        self.setFixedSize(520, 680)
        
        self.current_scale = 1
        self.output_dir = FileService.get_default_output_dir()
        
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.setup_title_bar(main_layout)
        self.setup_content(main_layout)
        self.setup_bottom_bar(main_layout)
    
    def setup_title_bar(self, parent_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.8);
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setPixmap(QIcon.fromTheme("image").pixmap(24, 24))
        
        title_label = QLabel("iOS 图片倍率处理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #1d1d1f;
            }
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()
        
        parent_layout.addWidget(title_bar)
    
    def setup_content(self, parent_layout):
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        scale_section = QWidget()
        scale_layout = QVBoxLayout(scale_section)
        scale_layout.setContentsMargins(0, 0, 0, 0)
        scale_layout.setSpacing(8)
        
        scale_label = QLabel("选择原图倍率")
        scale_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #1d1d1f;
            }
        """)
        
        self.scale_selector = ScaleSelectorWidget()
        self.scale_selector.scale_changed.connect(self.on_scale_changed)
        
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_selector)
        content_layout.addWidget(scale_section)
        
        self.drop_zone = DropZoneWidget()
        self.drop_zone.files_dropped.connect(self.on_files_dropped)
        self.drop_zone.browse_clicked.connect(self.on_browse_clicked)
        content_layout.addWidget(self.drop_zone)
        
        image_list_section = QWidget()
        image_list_layout = QVBoxLayout(image_list_section)
        image_list_layout.setContentsMargins(0, 0, 0, 0)
        image_list_layout.setSpacing(8)
        
        list_header_layout = QHBoxLayout()
        
        list_label = QLabel("已添加图片")
        list_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #1d1d1f;
            }
        """)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #007aff;
                border: none;
                font-size: 12px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background: rgba(0, 122, 255, 0.1);
                border-radius: 4px;
            }
        """)
        self.clear_btn.clicked.connect(self.on_clear_clicked)
        
        list_header_layout.addWidget(list_label)
        list_header_layout.addStretch()
        list_header_layout.addWidget(self.clear_btn)
        
        self.image_list = ImageListWidget()
        
        image_list_layout.addLayout(list_header_layout)
        image_list_layout.addWidget(self.image_list)
        content_layout.addWidget(image_list_section)
        
        parent_layout.addWidget(content_widget)
    
    def setup_bottom_bar(self, parent_layout):
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(100)
        bottom_bar.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.8);
                border-top: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        
        layout = QVBoxLayout(bottom_bar)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(12)
        
        output_row = QHBoxLayout()
        
        output_label = QLabel("输出目录")
        output_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #86868b;
            }
        """)
        
        self.output_path_label = QLabel(self.output_dir)
        self.output_path_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #1d1d1f;
            }
        """)
        self.output_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        browse_dir_btn = QPushButton("打开目录")
        browse_dir_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.8);
                color: #007aff;
                border: 1px solid #007aff;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(0, 122, 255, 0.05);
            }
        """)
        browse_dir_btn.clicked.connect(self.on_browse_dir_clicked)
        
        output_row.addWidget(output_label)
        output_row.addWidget(self.output_path_label)
        output_row.addWidget(browse_dir_btn)
        
        action_row = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 6px;
                border-radius: 3px;
                background: #e8e8ed;
            }
            QProgressBar::chunk {
                background: #007aff;
                border-radius: 3px;
            }
        """)
        self.progress_bar.setVisible(False)
        
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background: #007aff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 32px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066cc;
            }
            QPushButton:pressed {
                background: #0052aa;
            }
            QPushButton:disabled {
                background: #a0a0a0;
            }
        """)
        self.convert_btn.clicked.connect(self.on_convert_clicked)
        self.convert_btn.setCursor(Qt.PointingHandCursor)
        
        action_row.addWidget(self.progress_bar)
        action_row.addWidget(self.convert_btn)
        
        layout.addLayout(output_row)
        layout.addLayout(action_row)
        
        parent_layout.addWidget(bottom_bar)
    
    def on_scale_changed(self, scale):
        self.current_scale = scale
    
    def on_files_dropped(self, files):
        self.add_files(files)
    
    def on_browse_clicked(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.webp)"
        )
        if files:
            self.add_files(files)
    
    def add_files(self, files):
        for file_path in files:
            if ImageService.is_valid_image(file_path):
                detected_scale = ImageService.detect_scale_factor(file_path)
                info = ImageService.get_image_info(file_path)
                if info:
                    self.image_list.add_image(file_path, detected_scale, info)
        
        self.update_convert_button()
    
    def on_clear_clicked(self):
        self.image_list.clear_all()
        self.update_convert_button()
    
    def on_browse_dir_clicked(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_dir))
    
    def on_convert_clicked(self):
        items = self.image_list.get_items()
        if not items:
            QMessageBox.warning(self, "警告", "请先添加图片")
            return
        
        FileService.create_directory_if_not_exists(self.output_dir)
        
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = WorkerThread(items, self.output_dir)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.task_completed.connect(self.on_task_completed)
        self.worker.start()
    
    def on_progress_updated(self, value):
        self.progress_bar.setValue(value)
    
    def on_task_completed(self, success, message):
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.image_list.clear_all()
            self.update_convert_button()
        else:
            QMessageBox.error(self, "错误", message)
    
    def update_convert_button(self):
        count = self.image_list.count()
        self.convert_btn.setEnabled(count > 0)
