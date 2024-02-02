#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QScrollableGridWidget, QGridWidget, QIconWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel
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
        widget.grid_layout.setSpacing(0)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setRowStretch(2, 1)

        return widget


    def icon_with_text(self, icon: str = None, text: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(16)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty('title', True)
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        widget.icon_widget = QIconWidget(None, icon, QSize(40, 40), True)
        widget.grid_layout.addWidget(widget.icon_widget, 1, 0)
        widget.grid_layout.setAlignment(widget.icon_widget, Qt.AlignmentFlag.AlignCenter)

        widget.grid_layout.setRowStretch(2, 1)

        return widget


    def get(self) -> dict | None:
        return None
#----------------------------------------------------------------------
