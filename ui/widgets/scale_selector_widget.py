from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

class ScaleSelectorWidget(QWidget):
    scale_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_scale = 1
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.buttons = []
        
        scales = [1, 2, 3]
        for scale in scales:
            btn = QPushButton(f"@{scale}x")
            btn.setFixedWidth(80)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.5);
                    color: #86868b;
                    border: none;
                    border-radius: 0;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:checked {
                    background: #007aff;
                    color: white;
                }
                QPushButton:first-child {
                    border-radius: 8px 0 0 8px;
                }
                QPushButton:last-child {
                    border-radius: 0 8px 8px 0;
                }
                QPushButton:hover:not(:checked) {
                    background: rgba(255, 255, 255, 0.8);
                }
            """)
            btn.clicked.connect(lambda checked, s=scale: self.on_scale_selected(s))
            btn.setCursor(Qt.PointingHandCursor)
            
            if scale == 1:
                btn.setChecked(True)
            
            self.buttons.append(btn)
            layout.addWidget(btn)
    
    def on_scale_selected(self, scale):
        self.current_scale = scale
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i + 1 == scale)
        self.scale_changed.emit(scale)
    
    def get_scale(self):
        return self.current_scale
