from PyQt5.QtWidgets import QTextEdit, QSizePolicy
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import QSize


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)

        self.textChanged.connect(lambda: self.updateGeometry())

    def setMinimumLines(self, num_lines):

        self.setMinimumSize(self.minimumSize().width(),
                            self.lineCountToWidgetHeight(num_lines))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        margins = self.contentsMargins()

        if width >= margins.left() + margins.right():
            document_width = round(width - margins.left() - margins.right())
        else:
            document_width = 0

        document = self.document().clone()
        document.setTextWidth(document_width)

        return round(margins.top() + document.size().height() + margins.bottom())

    def sizeHint(self):
        original_hint = super().sizeHint()
        return QSize(original_hint.width(), self.heightForWidth(original_hint.width()))

    def lineCountToWidgetHeight(self, num_lines):
        assert num_lines >= 0

        widget_margins = self.contentsMargins()
        document_margin = self.document().documentMargin()
        font_metrics = QFontMetrics(self.document().defaultFont())

        return (
            widget_margins.top() +
            document_margin +
            max(num_lines, 1) * font_metrics.height() +
            self.document().documentMargin() +
            widget_margins.bottom()
        )

        return QSize(original_hint.width(), minimum_height_hint)
