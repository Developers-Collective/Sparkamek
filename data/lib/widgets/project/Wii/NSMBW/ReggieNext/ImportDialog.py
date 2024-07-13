#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QPushButton, QLabel
from PySide6.QtCore import Qt
from data.lib.QtUtils import QGridFrame, QLangData, QGridWidget, QNamedSpinBox
from .sprites import Sprite
#----------------------------------------------------------------------

    # Class
class ImportDialog(QDialog):
    def __init__(self, parent = None , lang: QLangData = {}, sprite: Sprite = None, i: int = 1, length: int = 1):
        super().__init__(parent)

        self.setWindowTitle(lang.get('title').replace('%s', sprite.sprite_name, 1).replace('%s', str(i), 1).replace('%s', str(length), 1))

        self._sprite = sprite.copy()

        self._root = QGridFrame(self)
        self._root.layout_.setContentsMargins(0, 0, 0, 0)
        self._root.layout_.setSpacing(0)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(16, 16, 16, 16)
        frame.layout_.setSpacing(16)
        self._root.layout_.addWidget(frame, 0, 0)
        self._root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignTop)

        label = ImportDialog._text_group(lang.get('QLabel.spriteID.title'), lang.get('QLabel.spriteID.description'))
        frame.layout_.addWidget(label, frame.layout_.count(), 0)

        self._sprite_id_spinbox = QNamedSpinBox(None, lang.get('QNamedSpinBox.spriteID'))
        self._sprite_id_spinbox.set_range(0, 2147483647) # profileID is u32 (2^32 - 1) but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will have 2^31 sprites lmao)
        self._sprite_id_spinbox.set_value(sprite.id)
        frame.layout_.addWidget(self._sprite_id_spinbox, frame.layout_.count(), 0)
        frame.layout_.setAlignment(self._sprite_id_spinbox, Qt.AlignmentFlag.AlignLeft)

        frame = QGridFrame()
        frame.layout_.setContentsMargins(20, 20, 20, 20)
        frame.layout_.setSpacing(0)
        frame.setProperty('border-top', True)
        self._root.layout_.addWidget(frame, 1, 0)
        self._root.layout_.setAlignment(frame, Qt.AlignmentFlag.AlignBottom)

        right_buttons = QGridFrame()
        right_buttons.layout_.setSpacing(16)
        right_buttons.layout_.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang.get('QPushButton.cancel'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.layout_.addWidget(button, 0, 0)

        button = QPushButton(lang.get('QPushButton.import'))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.layout_.addWidget(button, 0, 1)

        frame.layout_.addWidget(right_buttons, 0, 0)
        frame.layout_.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self._root.layout_)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 512)), int(parent.window().size().height() * (3 / 15)))

    def _text_group(title: str = '', description: str = '') -> QGridWidget:
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

    def exec(self) -> Sprite | None:
        if super().exec():
            self._sprite.id = self._sprite_id_spinbox.value()
            return self._sprite
        return None
#----------------------------------------------------------------------
