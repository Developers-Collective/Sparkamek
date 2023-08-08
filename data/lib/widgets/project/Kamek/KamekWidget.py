#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.widgets.ProjectKeys import ProjectKeys
from .CompilerDockWidget import CompilerDockWidget
#----------------------------------------------------------------------

    # Class
class KamekWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Kamek

    _lang = {}

    def init(app: QBaseApplication) -> None:
        KamekWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget')
        CompilerDockWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        # for i in range(100):
        #     self.scroll_layout.addWidget(QPushButton('Button {}'.format(i)), i, 0)

        self._compiler_dock_widget = CompilerDockWidget(app, name, icon, data)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._compiler_dock_widget)

        # if 'properties' in self.save_data.dock_widgets: self.properties_menu_dock_widget.load_dict(self.window, self.save_data.dock_widgets['properties'])
        # else: self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_menu_dock_widget)

    @property
    def task_is_running(self) -> bool:
        return self._compiler_dock_widget.task_is_running
#----------------------------------------------------------------------
