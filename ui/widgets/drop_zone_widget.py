from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QMouseEvent
from PySide6.QtCore import Qt, Signal

class DropZoneWidget(QWidget):
    files_dropped = Signal(list)
    browse_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon.fromTheme("image").pixmap(48, 48))
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        self.title_label = QLabel("拖拽图片到这里")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 500;
                color: #1d1d1f;
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.subtitle_label = QLabel("或点击选择图片")
        self.subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #86868b;
            }
        """)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        
        self.browse_btn = QPushButton("选择图片")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background: #007aff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066cc;
            }
            QPushButton:pressed {
                background: #0052aa;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_clicked)
        self.browse_btn.setFixedWidth(140)
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.browse_btn, 0, Qt.AlignCenter)
        
        self.update_styles()
    
    def update_styles(self):
        if self.is_dragging:
            self.setStyleSheet("""
                QWidget {
                    border: 2px dashed #007aff;
                    border-radius: 12px;
                    background: rgba(0, 122, 255, 0.05);
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    border: 2px dashed #d1d1d6;
                    border-radius: 12px;
                    background: rgba(255, 255, 255, 0.5);
                }
                QWidget:hover {
                    border-color: #007aff;
                    background: rgba(0, 122, 255, 0.02);
                }
            """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.is_dragging = True
            self.update_styles()
    
    def dragLeaveEvent(self, event: QDragEnterEvent):
        self.is_dragging = False
        self.update_styles()
    
    def dropEvent(self, event: QDropEvent):
        self.is_dragging = False
        self.update_styles()
        
        files = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                files.append(url.toLocalFile())
        
        if files:
            self.files_dropped.emit(files)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.browse_clicked.emit()
