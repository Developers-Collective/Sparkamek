#----------------------------------------------------------------------

    # Libraries
from data.lib.utils import AbstractFactory
from PySide6.QtWidgets import QWidget
#----------------------------------------------------------------------

    # Class
class WidgetFactory(AbstractFactory):
    @classmethod
    def register(cls_, key: str, cls: type[QWidget]) -> None:
        super().register(key, cls)

    @classmethod
    def create(cls, key: str, *args, **kwargs) -> QWidget:
        return super().create(key, *args, **kwargs)

    @classmethod
    def get(cls, key: str) -> type[QWidget]:
        return super().get(key)
#----------------------------------------------------------------------
