#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal
from ..BaseWidget import BaseWidget
#----------------------------------------------------------------------

    # Class
class BaseMenu(BaseWidget):
    can_continue_changed = Signal(bool)


    def __init__(self) -> None:
        super().__init__()
        self.scroll_layout.setContentsMargins(16, 16, 32, 16)


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(True)
#----------------------------------------------------------------------
