from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QListView

class ListView(QListView):

    def __init__(self, parent):
        super().__init__(parent=parent)

        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.setFont(font)

        self.setStyleSheet("""
            QListView{
                border: none;
                background-color: #0B1A30;
                outline: 0;
            }

            QListView::item{
                border: none;
                padding: 4px 6px;
            }

            QScrollBar:vertical{
                width: 8px;
                background: #0B1A30;
            }
            
            QScrollBar::handle:vertical{
                background-color: #97b9f4;    
                min-height: 5px;
            }
            
            QScrollBar::sub-line:vertical{
                height: 0;
                width: 0;
            }
            
            QScrollBar::add-line:vertical{
                height: 0;
                width: 0;
            }
            
            QScrollBar::add-page:vertical{
                background: none;
            }
            
            QScrollBar::sub-page:vertical{
                background: none;
            }
           
        """)
