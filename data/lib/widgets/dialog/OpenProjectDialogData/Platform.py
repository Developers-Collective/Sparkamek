#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QGridFrame, QBaseApplication, QLangData, QIconWidget, QBetterToolTip
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QMouseEvent, Qt
from data.lib.utils import AbstractTypeFactory
#----------------------------------------------------------------------

    # Class
@QBetterToolTip
class Platform(QGridFrame):
    _lang: QLangData = QLangData.NoTranslation()


    clicked = Signal()


    def init(app: QBaseApplication) -> None:
        Platform._lang = app.get_lang_data('OpenProjectDialog')


    def __init__(self, key: str, icon: str, game_factory: AbstractTypeFactory | type[AbstractTypeFactory]) -> None:
        super().__init__()

        self._key = key
        self._game_factory = game_factory() if isinstance(game_factory, type) else game_factory
        self.checked = False

        self.grid_layout.setSpacing(8)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._icon = QIconWidget(None, icon, QSize(120, 80), False)
        self.grid_layout.addWidget(self._icon, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self._title = QLabel(self._lang.get(f'platform.{key}') if key else self._lang.get('platform.unknown'))
        self._title.setProperty('h', 3)
        self.grid_layout.addWidget(self._title, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.setToolTip(self._title.text())

        self.grid_layout.setRowStretch(2, 1)

        self.setProperty('PlatformButton', True)
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
    def game_factory(self) -> AbstractTypeFactory:
        return self._game_factory


    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        self.checked = True
        self.clicked.emit()
#----------------------------------------------------------------------
