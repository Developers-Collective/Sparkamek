#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QGridWidget
#----------------------------------------------------------------------

    # Class
class ItemDataPropertyDockWidget(QSavableDockWidget):
    _lang = {}

    def init(app: QBaseApplication) -> None:
        ItemDataPropertyDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.ItemDataPropertyDockWidget')

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', str(None)))

        self._root = QScrollableGridWidget()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.scroll_widget.setProperty('QDockWidget', True)
        self.setObjectName('itemDataProperty')
        self.setWidget(self._root)

        self.update_title(None)

    def update_title(self, type: str | None) -> None:
        self.setWindowTitle(self._lang.get_data('title').replace('%s', f'{type}') if type else self._lang.get_data('title').replace('%s', str(None)))

    def set_widget(self, widget: QGridWidget | None) -> None:
        self.update_title(widget.type if widget else None)

        while self._root.scroll_widget.layout().count():
            self._root.scroll_widget.layout().takeAt(0).widget().setParent(None)

        if widget: self._root.scroll_layout.addWidget(widget, 0, 0)
#----------------------------------------------------------------------
