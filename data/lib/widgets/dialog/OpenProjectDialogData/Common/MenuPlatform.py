#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.QtUtils import QLangData, QGridFrame, QBaseApplication, QFlowScrollableWidget
from .BaseMenu import BaseMenu
from ..PlatformFactory import PlatformFactory
from ..Platform import Platform
#----------------------------------------------------------------------

    # Class
class MenuPlatform(BaseMenu):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        MenuPlatform._lang = app.get_lang_data('OpenProjectDialog.QSlidingStackedWidget.platform')
        PlatformFactory.init(app)


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


        label = self._text_group(lang.get('QLabel.platform.title'), lang.get('QLabel.platform.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        self._flow_widget = QFlowScrollableWidget(None, Qt.Orientation.Horizontal, 16, 8)
        root_frame.layout_.addWidget(self._flow_widget, root_frame.layout_.count(), 0)

        self._platforms = tuple(PlatformFactory.create(p) for p in PlatformFactory.get_all())
        send_param = lambda s: lambda: self.select_platform(s)
        for p in self._platforms:
            self._flow_widget.layout_.addWidget(p)
            p.clicked.connect(send_param(p.key))


    @property
    def selected_platform(self) -> Platform | None:
        for p in self._platforms:
            if p.checked:
                return p

        return None


    def select_platform(self, key: str) -> None:
        for p in self._platforms:
            p.checked = p.key == key

        self.update_continue()


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(self.selected_platform is not None)
#----------------------------------------------------------------------
