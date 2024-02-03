#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.qtUtils import QLangData, QGridFrame, QBaseApplication, QFlowScrollableWidget
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

        self.scroll_layout.setSpacing(30)

        topframe = QGridFrame()
        topframe.grid_layout.setSpacing(8)
        topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addWidget(topframe, self.scroll_layout.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.grid_layout.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.grid_layout.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addWidget(root_frame, self.scroll_layout.count(), 0)
        self.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.platform.title'), lang.get('QLabel.platform.description'))
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self._flow_widget = QFlowScrollableWidget(None, Qt.Orientation.Horizontal, 16, 8)
        root_frame.grid_layout.addWidget(self._flow_widget, root_frame.grid_layout.count(), 0)

        self._platforms = tuple(PlatformFactory.create(p) for p in PlatformFactory.get_all())
        send_param = lambda s: lambda: self.select_platform(s)
        for p in self._platforms:
            self._flow_widget.scroll_layout.addWidget(p)
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
