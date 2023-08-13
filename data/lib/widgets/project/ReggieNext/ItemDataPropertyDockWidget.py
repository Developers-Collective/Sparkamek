#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import Qt, QSortFilterProxyModel, Signal
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QGridWidget, QIconLineEdit, QUtilsColor, QBetterListWidget, QSaveData, DelayedSignal
from .SpriteListLoaderWorker import SpriteListLoaderWorker
from .sprites import *
#----------------------------------------------------------------------

    # Class
class ItemDataPropertyDockWidget(QSavableDockWidget):
    _lang = {}

    def init(app: QBaseApplication) -> None:
        ItemDataPropertyDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.ItemDataPropertyDockWidget')

        SpriteListLoaderWorker.init(app)

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

    def update_title(self, sprite: Sprite) -> None:
        self.setWindowTitle(self._lang.get_data('title').replace('%s', f'[{sprite.id}] {sprite.name}') if sprite else self._lang.get_data('title').replace('%s', str(None)))

    def set_widget(self, widget: QGridWidget | None) -> None:
        while self._root.scroll_widget.layout().count():
            self._root.scroll_widget.layout().takeAt(0).widget().setParent(None)

        if widget: self._root.scroll_layout.addWidget(widget, 0, 0)
#----------------------------------------------------------------------
