#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QTabWidget, QSizePolicy, QWidget, QPushButton, QMenu
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QIcon, QAction
from data.lib.QtUtils import QGridWidget, QSlidingStackedWidget, QBaseApplication, QSaveData, QLangData
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

    _lang: QLangData = QLangData.NoTranslation()

    _base_app: QBaseApplication = None
    _more_icon = None
    _show_in_explorer_icon = None
    _reset_dockwidgets_icon = None
    _edit_icon = None
    _remove_icon = None

    @staticmethod
    def init(app: QBaseApplication) -> None:
        Project._base_app = app
        Project._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects')
        Project._more_icon = QIcon(f'{app.save_data.get_icon_dir()}pushbutton/more.png')
        Project._show_in_explorer_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/showInExplorer.png')
        Project._reset_dockwidgets_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/resetDockWidgets.png')
        Project._edit_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/edit.png')
        Project._remove_icon = QIcon(f'{app.save_data.get_icon_dir()}popup/remove.png')

        for cls in ProjectType.get_all():
            cls.init(app)


    def __init__(self, project: dict = None, name: str = '', icon: str = '', platform: str = '', game: str = '') -> None:
        super().__init__()

        self._load_project(project, name, icon, platform, game)

        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self._build()

    def _build(self) -> None:
        top_frame = QGridWidget()
        top_frame.layout_.setContentsMargins(16, 16, 16, 0)
        top_frame.layout_.setSpacing(0)
        self.layout_.addWidget(top_frame, 0, 0)

        self._notebook = QTabWidget()
        self._notebook.tabBar().setProperty('color', 'main')
        self._notebook.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._notebook.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        top_frame.layout_.addWidget(self._notebook, 0, 0)

        self._notebook_tabs = QSlidingStackedWidget()
        self._notebook_tabs.set_orientation(Qt.Orientation.Horizontal)
        self.layout_.addWidget(self._notebook_tabs, 1, 0)

        self._tabs: dict[int, Project.TabInfo] = {}

        for w in self._projects:
            tab = w.type
            widget = QWidget()
            widget.setFixedHeight(1)
            i = self._notebook.addTab(widget, self._lang['QTabWidget'][tab])

            gw = QGridWidget()
            gw.layout_.setContentsMargins(0, 0, 0, 0)
            gw.layout_.addWidget(w)
            self._notebook_tabs.addWidget(gw)
            gw.layout_.setAlignment(gw, Qt.AlignmentFlag.AlignTop)
            gw.layout_.setSpacing(1)

            self._tabs[tab] = Project.TabInfo(gw, tab, i)

        self._notebook.currentChanged.connect(self._tab_switch_index)

        self._more_button = QPushButton()
        self._more_button.setProperty('color', 'main')
        self._more_button.setIcon(self._more_icon)
        self._more_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._more_button.clicked.connect(self._create_more_popup)
        self._more_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        top_frame.layout_.addWidget(self._more_button, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

    def rebuild(self, project: dict, name: str, icon: str, platform: str, game: str) -> None:
        while self.layout_.count() > 0:
            w = self.layout_.itemAt(0).widget()
            if w:
                self.layout_.removeWidget(w)
                w.deleteLater()

        self._load_project(project, name, icon, platform, game)
        self._build()

    def _load_project(self, project: dict, name: str, icon: str, platform: str, game: str) -> None:
        self._name = name
        self._icon = icon
        self._platform = platform
        self._game = game
        self._projects: list[SubProjectWidgetBase] = []

        for cls in ProjectType.get_all():
            if instance := cls(self._base_app, name, icon, project[cls.type]) if project.get(cls.type, None) else None:
                self._projects.append(instance)

    def save_project(self) -> dict:
        index = 0
        dct = {}

        for k in ProjectType.get_all_keys():
            if k == self._projects[index].type:
                dct[k] = self._projects[index].export()
                if len(self._projects) > index + 1: index += 1

            else:
                dct[k] = None

        return {
            'name': self._name,
            'icon': self._icon,
            'platform': self._platform,
            'game': self._game,
            'data':
                {
                    type: project.export() for type, project in [
                        (p.type, p) for p in self._projects
                    ]
                }
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
            action_showInExplorer = QAction(lang['QAction'][f'showInExplorer.{p.type}'])
            action_showInExplorer.setIcon(self._show_in_explorer_icon)
            action_showInExplorer.triggered.connect(send_param(p))
            actions_showInExplorer.append(action_showInExplorer)

        for a in actions_showInExplorer: menu.addAction(a) # Doesn't work if I do it in the loop above for some reason
        if actions_showInExplorer: menu.addSeparator()

        action_reset_dockwidgets = QAction(lang['QAction']['resetDockWidgets'])
        action_reset_dockwidgets.setIcon(self._reset_dockwidgets_icon)
        action_reset_dockwidgets.triggered.connect(self._reset_dockwidgets)
        menu.addAction(action_reset_dockwidgets)

        menu.addSeparator()

        action_edit = QAction(lang['QAction']['edit'])
        if self.task_is_running: action_edit.setEnabled(False)
        action_edit.setIcon(self._edit_icon)
        action_edit.triggered.connect(self._edit)
        menu.addAction(action_edit)

        menu.addSeparator()

        action_remove = QAction(lang['QAction']['remove'])
        if self.task_is_running: action_remove.setEnabled(False)
        action_remove.setIcon(self._remove_icon)
        action_remove.triggered.connect(self._remove)
        menu.addAction(action_remove)

        menu.exec(self._more_button.mapToGlobal(QPoint(0, 0)))

    def _show_in_explorer(self, w: SubProjectWidgetBase) -> None:
        if not w: return
        path = w.path.replace('/', '\\')
        subprocess.Popen(rf'explorer /select, "{path}"', shell = False)

    def _reset_dockwidgets(self) -> None:
        for p in self._projects:
            p.reset_dock_widgets()

    def _edit(self) -> None:
        if self.task_is_running: return
        self.edit_clicked.emit()

    def _remove(self) -> None:
        if self.task_is_running: return
        self.remove_clicked.emit()

    @property
    def task_is_running(self) -> bool:
        for p in self._projects:
            if p.task_is_running: return True
        return False

    def settings_updated(self, settings: QSaveData) -> None:
        for p in self._projects:
            p.settings_updated(settings)
#----------------------------------------------------------------------
