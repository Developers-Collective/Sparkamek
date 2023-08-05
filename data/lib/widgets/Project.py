#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTabWidget, QSizePolicy, QWidget
from PySide6.QtCore import Qt, QEvent
from data.lib.qtUtils import QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QBaseApplication
from .ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class Project(QGridWidget):
    class TabInfo:
        def __init__(self, widget: QWidget, key: str, index: str) -> None:
            self.widget = widget
            self.key = key
            self.index = index


    _lang = {}

    @staticmethod
    def init(app: QBaseApplication) -> None:
        Project._lang = app.save_data.language_data['QMainWindow']['QSlidingStackedWidget']['mainMenu']['projects']


    def __init__(self, parent = None, project: dict = None) -> None:
        super().__init__(parent)
        self._load_project(project)

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self._notebook = QTabWidget()
        self._notebook.tabBar().setProperty('color', 'main')
        self._notebook.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._notebook.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_layout.addWidget(self._notebook, 0, 0)

        self._notebook_tabs = QSlidingStackedWidget()
        self._notebook_tabs.set_orientation(Qt.Orientation.Horizontal)
        self.grid_layout.addWidget(self._notebook_tabs, 1, 0)

        self._tabs: dict[int, Project.TabInfo] = {}

        for tab in [s for s in ['loader', 'kamek', 'reggieNext'] if project[s]]:
            widget = QWidget()
            widget.setFixedHeight(1)
            i = self._notebook.addTab(widget, self._lang['QTabWidget'][tab])

            sw = QScrollableGridWidget()
            self._notebook_tabs.addWidget(sw)
            sw.scroll_layout.setAlignment(sw, Qt.AlignmentFlag.AlignTop)
            sw.scroll_layout.setSpacing(1)

            self._tabs[tab] = Project.TabInfo(sw, tab, i)

        self._notebook.currentChanged.connect(self.tab_switch_index)

    def _load_project(self, project: dict) -> None:
        self._loader_file = project[ProjectKeys.Loader]
        self._kamek_file = project[ProjectKeys.Kamek]
        self._reggie_folder = project[ProjectKeys.Reggie]

    def save_project(self) -> dict:
        return {
            ProjectKeys.Loader: self._loader_file,
            ProjectKeys.Kamek: self._kamek_file,
            ProjectKeys.Reggie: self._reggie_folder
        }

    def tab_switch_index(self, index: int) -> None:
        self._notebook_tabs.slide_in_index(index)
#----------------------------------------------------------------------
