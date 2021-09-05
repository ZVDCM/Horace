from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtCore import Qt

class TableView(QTableView):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.verticalHeader().setMinimumSectionSize(40)
        self.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.setWordWrap(False)
        self.setStyleSheet("""
            QTableView {
                outline: 0;
                border: 1px solid #0e4884;
                gridline-color: #97b9f4;
            }

            QTableView::item:selected:active {
                border: none;
                background: #0078D7;
            }

            QTableView::item:selected:!active {
                border: none;
                background: white;
                color: black;
            }

            QHeaderView::section {
                background-color: #0d3c6e;
                border-top: 0px solid #97b9f4;
                border-bottom: 1px solid #97b9f4;
                border-right: 1px solid #97b9f4;
            }
            
            QTableCornerButton::section{
                background-color: #0d3c6e;
                border-top: 0px solid #97b9f4;
                border-bottom: 1px solid #97b9f4;
                border-right: 1px solid #97b9f4;
            }
            
            QScrollBar:horizontal{
                height: 9px;
            }
            
            QScrollBar:vertical{
                width: 9px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical{
                background-color: #97b9f4;    
                width: 18px;
            }
            
            QScrollBar::handle:horizontal{
                background-color: #97b9f4;    
                min-width: 5px;
            }
            
            QScrollBar::sub-line:horizontal,
            QScrollBar::sub-line:vertical{
                height: 0;
                width: 0;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::add-line:vertical{
                height: 0;
                width: 0;
            }
            
            QScrollBar::add-page:horizontal{
                background: #102542;
                margin-left: -3px;
            }
            
            QScrollBar::add-page:vertical{
                background: #102542;
                margin-top: -3px;
            }
            
            QScrollBar::sub-page:horizontal{
                background: #102542;
                margin-right: -3px;
            }
            
            QScrollBar::sub-page:vertical{
                background: #102542;
                margin-bottom: -3px;
            }
        """)