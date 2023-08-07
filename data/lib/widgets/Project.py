#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTabWidget, QSizePolicy, QWidget, QPushButton, QMenu, QMainWindow
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QIcon, QAction
from data.lib.qtUtils import QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QBaseApplication
from .ProjectKeys import ProjectKeys
from .project import *

import subprocess
#----------------------------------------------------------------------

    # Class
class Project(QGridWidget):
    class TabInfo:
        def __init__(self, widget: QWidget, key: str, index: str) -> None:
            self.widget = widget
            self.key = key
            self.index = index

    edit_clicked = Signal()
    remove_clicked = Signal()

    _lang = {}

    _base_app: QBaseApplication = None
    _more_icon = None
    _show_in_explorer_icon = None
    _edit_icon = None
    _remove_icon = None

    @staticmethod
    def init(app: QBaseApplication) -> None:
        Project._base_app = app
        Project._lang = app.save_data.language_data['QMainWindow']['QSlidingStackedWidget']['mainMenu']['projects']
        Project._more_icon = QIcon(f'{app.save_data.get_icon_dir()}pushbutton/more.png')
        Project._show_in_explorer_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/showInExplorer.png')
        Project._edit_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/edit.png')
        Project._remove_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/remove.png')


    def __init__(self, project: dict = None, name: str = '', icon: str = '') -> None:
        super().__init__()

        self._load_project(project, name, icon)

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self._build(project)

    def _build(self, project: dict) -> None:
        top_frame = QGridWidget()
        top_frame.grid_layout.setContentsMargins(16, 16, 16, 0)
        top_frame.grid_layout.setSpacing(0)
        self.grid_layout.addWidget(top_frame, 0, 0)

        self._notebook = QTabWidget()
        self._notebook.tabBar().setProperty('color', 'main')
        self._notebook.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._notebook.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        top_frame.grid_layout.addWidget(self._notebook, 0, 0)

        self._notebook_tabs = QSlidingStackedWidget()
        self._notebook_tabs.set_orientation(Qt.Orientation.Horizontal)
        self.grid_layout.addWidget(self._notebook_tabs, 1, 0)

        self._tabs: dict[int, Project.TabInfo] = {}

        for tab, w in [
            s for s in [
                (ProjectKeys.Loader.value, self._loader),
                (ProjectKeys.Kamek.value, self._kamek),
                (ProjectKeys.ReggieNext.value, self._reggie_next),
                (ProjectKeys.Riivolution.value, self._riivolution)
            ] if project.get(s[0], None)
        ]:
            widget = QWidget()
            widget.setFixedHeight(1)
            i = self._notebook.addTab(widget, self._lang['QTabWidget'][tab])

            gw = QGridWidget()
            gw.grid_layout.setContentsMargins(0, 0, 0, 0)
            gw.grid_layout.addWidget(w)
            self._notebook_tabs.addWidget(gw)
            gw.grid_layout.setAlignment(gw, Qt.AlignmentFlag.AlignTop)
            gw.grid_layout.setSpacing(1)

            self._tabs[tab] = Project.TabInfo(gw, tab, i)

        self._notebook.currentChanged.connect(self._tab_switch_index)

        self._more_button = QPushButton()
        self._more_button.setProperty('color', 'main')
        self._more_button.setIcon(self._more_icon)
        self._more_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._more_button.clicked.connect(self._create_more_popup)
        self._more_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        top_frame.grid_layout.addWidget(self._more_button, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

    def rebuild(self, project: dict) -> None:
        while self.grid_layout.count() > 0:
            w = self.grid_layout.itemAt(0).widget()
            if w:
                self.grid_layout.removeWidget(w)
                w.deleteLater()

        self._load_project(project)
        self._build(project)

    def _load_project(self, project: dict, name: str, icon: str) -> None:
        self._loader = LoaderWidget(self._base_app, name, icon, project[ProjectKeys.Loader]) if project.get(ProjectKeys.Loader, None) else None
        self._kamek = KamekWidget(self._base_app, name, icon, project[ProjectKeys.Kamek]) if project.get(ProjectKeys.Kamek, None) else None
        self._reggie_next = ReggieNextWidget(self._base_app, name, icon, project[ProjectKeys.ReggieNext]) if project.get(ProjectKeys.ReggieNext, None) else None
        self._riivolution = RiivolutionWidget(self._base_app, name, icon, project[ProjectKeys.Riivolution]) if project.get(ProjectKeys.Riivolution, None) else None

    def save_project(self) -> dict:
        return {
            ProjectKeys.Loader.value: self._loader.export() if self._loader else None,
            ProjectKeys.Kamek.value: self._kamek.export() if self._kamek else None,
            ProjectKeys.ReggieNext.value: self._reggie_next.export() if self._reggie_next else None,
            ProjectKeys.Riivolution.value: self._riivolution.export() if self._riivolution else None
        }

    def _tab_switch_index(self, index: int) -> None:
        self._notebook_tabs.slide_in_index(index)

    def _create_more_popup(self) -> None:
        lang = self._lang['QMenu']['more']

        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        need_separator = False

        if self._loader:
            action_showLoaderInExplorer = QAction(lang['QAction']['showLoaderInExplorer'])
            action_showLoaderInExplorer.setIcon(self._show_in_explorer_icon)
            action_showLoaderInExplorer.triggered.connect(lambda: self._show_in_explorer(self._loader))
            menu.addAction(action_showLoaderInExplorer)
            need_separator = True

        if self._kamek:
            action_showKamekInExplorer = QAction(lang['QAction']['showKamekInExplorer'])
            action_showKamekInExplorer.setIcon(self._show_in_explorer_icon)
            action_showKamekInExplorer.triggered.connect(lambda: self._show_in_explorer(self._kamek))
            menu.addAction(action_showKamekInExplorer)
            need_separator = True

        if self._reggie_next:
            action_showReggieNextInExplorer = QAction(lang['QAction']['showReggieNextInExplorer'])
            action_showReggieNextInExplorer.setIcon(self._show_in_explorer_icon)
            action_showReggieNextInExplorer.triggered.connect(lambda: self._show_in_explorer(self._reggie_next))
            menu.addAction(action_showReggieNextInExplorer)
            need_separator = True

        if self._riivolution:
            action_showRiivolutionInExplorer = QAction(lang['QAction']['showRiivolutionInExplorer'])
            action_showRiivolutionInExplorer.setIcon(self._show_in_explorer_icon)
            action_showRiivolutionInExplorer.triggered.connect(lambda: self._show_in_explorer(self._riivolution))
            menu.addAction(action_showRiivolutionInExplorer)
            need_separator = True

        if need_separator: menu.addSeparator()

        action_edit = QAction(lang['QAction']['edit'])
        action_edit.setIcon(self._edit_icon)
        action_edit.triggered.connect(self._edit)
        menu.addAction(action_edit)

        menu.addSeparator()

        action_remove = QAction(lang['QAction']['remove'])
        action_remove.setIcon(self._remove_icon)
        action_remove.triggered.connect(lambda: self.remove_clicked.emit())
        menu.addAction(action_remove)

        menu.exec(self._more_button.mapToGlobal(QPoint(0, 0)))

    def _show_in_explorer(self, w: SubProjectWidgetBase) -> None:
        if not w: return
        path = w.path.replace('/', '\\')
        subprocess.Popen(rf'explorer /select, "{path}"', shell = False)

    def _edit(self) -> None:
        self.edit_clicked.emit()
#----------------------------------------------------------------------
