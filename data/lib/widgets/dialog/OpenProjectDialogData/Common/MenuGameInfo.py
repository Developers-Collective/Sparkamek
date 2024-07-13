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

        self.layout_.setContentsMargins(0, 0, 0, 0)


    def set_game(self, widget: GameInfo) -> None:
        for i in reversed(range(self.layout_.count())):
            item = self.layout_.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.layout_.removeItem(item)

        self._widget = widget
        self.layout_.addWidget(self._widget, 0, 0)


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(True)


    def export(self) -> dict:
        return self._widget.export() if self._widget else {}
#----------------------------------------------------------------------
