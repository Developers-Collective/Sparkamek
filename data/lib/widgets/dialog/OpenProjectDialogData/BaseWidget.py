#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QScrollableGridWidget, QGridWidget, QIconWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QLabel
#----------------------------------------------------------------------

    # Class
class BaseWidget(QScrollableGridWidget):
    _forbidden_paths = (
        None,
        '',
        '.',
        './'
    )


    def __init__(self) -> None:
        super().__init__()


    def _text_group(self, title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(0)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.layout_.addWidget(label, 1, 0)
        widget.layout_.setRowStretch(2, 1)

        return widget


    def icon_with_text(self, icon: str = None, text: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.layout_.setSpacing(16)
        widget.layout_.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.layout_.addWidget(label, 0, 0)
        widget.layout_.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = QIconWidget(None, icon, QSize(40, 40), True)
        widget.layout_.addWidget(widget.icon_widget, 1, 0)
        widget.layout_.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.layout_.setRowStretch(2, 1)

        return widget


    def export(self) -> dict | None:
        return None
#----------------------------------------------------------------------
