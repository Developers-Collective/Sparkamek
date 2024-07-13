#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QGridFrame, QIconWidget, QBaseApplication, QLangData, QBetterToolTip
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel
from .GameInfo import GameInfo
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class Game(QGridFrame):
    _lang: QLangData = QLangData.NoTranslation()


    clicked = Signal()


    def init(app: QBaseApplication) -> None:
        Game._lang = app.get_lang_data('OpenProjectDialog')


    def __init__(self, key: str, icon: str, game_info: type[GameInfo]) -> None:
        super().__init__()

        self._key = key
        self._game_info = game_info
        self.checked = False

        self.layout_.setSpacing(8)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self._icon = QIconWidget(None, icon, QSize(120, 80), False)
        self.layout_.addWidget(self._icon, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self._title = QLabel(self._lang.get(f'game.{key}.title') if key else self._lang.get('game.unknown'))
        self._title.setProperty('h', 3)
        self.layout_.addWidget(self._title, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.setToolTip(self._title.text())

        self.layout_.setRowStretch(2, 1)

        self.setProperty('GameButton', True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedWidth(180)
        self.setFixedHeight(120)


    @property
    def checked(self) -> bool:
        return self._checked
    
    @checked.setter
    def checked(self, value: bool) -> None:
        self._checked = value
        self.setProperty('checked', value)

        self.style().unpolish(self)
        self.style().polish(self)


    @property
    def key(self) -> str:
        return self._key


    @property
    def game_info(self) -> type[GameInfo]:
        return self._game_info


    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        self.checked = True
        self.clicked.emit()
#----------------------------------------------------------------------
