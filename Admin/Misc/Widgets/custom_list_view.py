from PyQt5.QtWidgets import QListView
from PyQt5 import QtGui

class ListView(QListView):

    def __init__(self, parent):
        super().__init__(parent=parent)

        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.setFont(font)

        self.setStyleSheet("""
            QListView{
                border: 1px solid #0e4884;
                background: #072f49;
                outline: 0;
            }

            QListView::item{
                border: none;
                padding: 4px 6px;
                margin-bottom: 5px;
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
           
        """)


