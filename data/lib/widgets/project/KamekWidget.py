#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget
from .SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.widgets.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class KamekWidget(SubProjectWidgetBase):
    type: ProjectKeys = ProjectKeys.Kamek

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(app, data)

        # for i in range(100):
        #     self.scroll_layout.addWidget(QPushButton('Button {}'.format(i)), i, 0)

        self._compiler = QScrollableGridWidget()
        self._compiler.setProperty('wide', True)
        self._compiler.setMinimumWidth(200)
        self._compiler.setMinimumHeight(100)
        self._compiler.setFrameShape(QFrame.Shape.NoFrame)
        self._compiler.scroll_widget.setProperty('QDockWidget', True)

        self._compiler_dock_widget = QSavableDockWidget('Compiler')
        self._compiler_dock_widget.setObjectName('compiler')
        self._compiler_dock_widget.setWidget(self._compiler)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._compiler_dock_widget)

        # if 'properties' in self.save_data.dock_widgets: self.properties_menu_dock_widget.load_dict(self.window, self.save_data.dock_widgets['properties'])
        # else: self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_menu_dock_widget)
#----------------------------------------------------------------------
