#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget
from ..SubProjectWidgetBase import SubProjectWidgetBase
from data.lib.widgets.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class CompilerDockWidget(QSavableDockWidget):
    _lang = {}

    def init(app: QBaseApplication) -> None:
        CompilerDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.CompilerDockWidget')

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', name))

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('compiler')
        self.setWidget(self._root)
#----------------------------------------------------------------------
