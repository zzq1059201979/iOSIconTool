from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFrame, QSizePolicy
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

class ImageItemWidget(QWidget):
    def __init__(self, file_path, scale, info, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.scale = scale
        
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.7);
                border-radius: 8px;
                padding: 8px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.9);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(64, 64)
        self.thumbnail_label.setScaledContents(True)
        self.thumbnail_label.setStyleSheet("border-radius: 4px;")
        
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.thumbnail_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        layout.addWidget(self.thumbnail_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        self.name_label = QLabel(file_path.split('/')[-1])
        self.name_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #1d1d1f;")
        
        self.info_label = QLabel(f"{info['width']} × {info['height']} | @{scale}x")
        self.info_label.setStyleSheet("font-size: 11px; color: #86868b;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.info_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.remove_btn = QPushButton()
        self.remove_btn.setIcon(QIcon.fromTheme("trash"))
        self.remove_btn.setFixedSize(24, 24)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 4px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.1);
            }
            QPushButton:pressed {
                background: rgba(239, 68, 68, 0.2);
            }
        """)
        layout.addWidget(self.remove_btn)

class ImageListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
                spacing: 8px;
            }
            QListWidget::item {
                border: none;
                padding: 0;
            }
        """)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        
        layout.addWidget(self.list_widget)
    
    def add_image(self, file_path, scale, info):
        item = QListWidgetItem()
        widget = ImageItemWidget(file_path, scale, info)
        widget.remove_btn.clicked.connect(lambda: self.remove_item(item))
        
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)
    
    def remove_item(self, item):
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)
    
    def clear_all(self):
        self.list_widget.clear()
    
    def count(self):
        return self.list_widget.count()
    
    def get_items(self):
        items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget:
                items.append({
                    'file_path': widget.file_path,
                    'scale': widget.scale
                })
        return items
