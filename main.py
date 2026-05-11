import sys
import os

os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 247))
    palette.setColor(QPalette.WindowText, QColor(29, 29, 31))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 247))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(29, 29, 31))
    palette.setColor(QPalette.Text, QColor(29, 29, 31))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(29, 29, 31))
    palette.setColor(QPalette.BrightText, QColor(255, 68, 68))
    palette.setColor(QPalette.Link, QColor(0, 122, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 122, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
