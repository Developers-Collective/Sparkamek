#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.QtUtils import QLangData, QGridFrame, QBaseApplication, QFlowScrollableWidget
from data.lib.utils import AbstractTypeFactory
from .BaseMenu import BaseMenu
from ..Game import Game
#----------------------------------------------------------------------

    # Class
class MenuGame(BaseMenu):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        MenuGame._lang = app.get_lang_data('OpenProjectDialog.QSlidingStackedWidget.game')


    def __init__(self, data: dict) -> None:
        super().__init__()

        lang = self._lang

        self.layout_.setSpacing(30)

        topframe = QGridFrame()
        topframe.layout_.setSpacing(8)
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(topframe, self.layout_.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.layout_.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.layout_.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(root_frame, self.layout_.count(), 0)
        self.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.game.title'), lang.get('QLabel.game.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        self._flow_widget = QFlowScrollableWidget(None, Qt.Orientation.Horizontal, 16, 8)
        root_frame.layout_.addWidget(self._flow_widget, root_frame.layout_.count(), 0)

        self._factory = None
        self._games = tuple()


    def set_factory(self, factory: AbstractTypeFactory) -> None:
        self._factory = factory

        self._flow_widget.clear()

        self._games = tuple(factory.create(p) for p in factory.get_all())
        send_param = lambda s: lambda: self.select_game(s)
        for p in self._games:
            self._flow_widget.layout_.addWidget(p)
            p.clicked.connect(send_param(p.key))

        self._flow_widget.setFixedHeight(self._flow_widget.layout_.sizeHint().height() + 32)


    @property
    def selected_game(self) -> Game | None:
        for p in self._games:
            if p.checked:
                return p

        return None


    def select_game(self, key: str) -> None:
        for p in self._games:
            p.checked = p.key == key

        self.update_continue()


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(self.selected_game is not None)
#----------------------------------------------------------------------
