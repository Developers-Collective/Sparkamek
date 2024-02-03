#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal
from .BaseMenu import BaseMenu
from ..GameInfo import GameInfo
#----------------------------------------------------------------------

    # Class
class MenuGameInfo(BaseMenu):
    can_continue_changed = Signal(bool)


    def __init__(self, data: dict) -> None:
        super().__init__()
        self._data = data
        self._widget: type[GameInfo] = None

        self.scroll_layout.setContentsMargins(0, 0, 0, 0)


    def set_game(self, widget: GameInfo) -> None:
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.scroll_layout.removeItem(item)

        self._widget = widget
        self.scroll_layout.addWidget(self._widget, 0, 0)


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(True)
#----------------------------------------------------------------------
