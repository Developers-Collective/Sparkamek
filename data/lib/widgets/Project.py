#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTabWidget, QSizePolicy, QWidget, QPushButton, QMenu, QMainWindow
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QIcon, QAction
from data.lib.qtUtils import QGridWidget, QSlidingStackedWidget, QScrollableGridWidget, QBaseApplication
from .ProjectKeys import ProjectKeys
from .ProjectType import ProjectType
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

        for w in self._projects:
            tab = w.type.value
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
        self._projects: list[SubProjectWidgetBase] = []

        for cls in ProjectType.get_all():
            if instance := cls(self._base_app, name, icon, project[cls.type]) if project.get(cls.type, None) else None:
                self._projects.append(instance)

    def save_project(self) -> dict:
        index = 0
        dct = {}

        for k in ProjectType.get_all_keys():
            if k == self._projects[index].type:
                dct[k.value] = self._projects[index].export()
                if len(self._projects) > index + 1: index += 1

            else:
                dct[k.value] = None

        return {
            type: project.export() for type, project in [
                (p.type.value, p) for p in self._projects
            ]
        }

    def _tab_switch_index(self, index: int) -> None:
        self._notebook_tabs.slide_in_index(index)

    def _create_more_popup(self) -> None:
        lang = self._lang['QMenu']['more']

        menu = QMenu(self)
        menu.setCursor(Qt.CursorShape.PointingHandCursor)

        send_param = lambda i: lambda: self._show_in_explorer(i)
        actions_showInExplorer = []

        for p in self._projects:
            action_showInExplorer = QAction(lang['QAction'][f'show{p.type.value[0].upper() + p.type.value[1:]}InExplorer'])
            action_showInExplorer.setIcon(self._show_in_explorer_icon)
            action_showInExplorer.triggered.connect(send_param(p))
            actions_showInExplorer.append(action_showInExplorer)

        for a in actions_showInExplorer: menu.addAction(a) # Doesn't work if I do it in the loop above for some reason
        if actions_showInExplorer: menu.addSeparator()

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
