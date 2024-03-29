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
                padding: 8px;
            }

            QListView::item:hover{
                background: #06293f;
            }

            QListView::item:selected{
                background: #256eff;
            }

            QListView::item:selected:active{
                background: #256eff;
            }

            QListView::item:selected:!active{
                background: white;
            }

            QListView::item:disabled{
                color: #6b6b6b;
            }

            QScrollBar:vertical{
                width: 8px;
                background: #102542;
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


class ReadOnlyListView(QListView):

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
                background: #102542;
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
