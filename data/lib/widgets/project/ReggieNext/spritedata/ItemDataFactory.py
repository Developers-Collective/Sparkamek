#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication
from .BaseItemData import BaseItemData
from . import *
#----------------------------------------------------------------------

    # Class
class ItemDataFactory:
    _app: QBaseApplication = None
    _data: dict[str, BaseItemData] = {}

    _spritedatas: list[type[BaseItemData]] = [ # Too lazy to make it dynamic
        CheckBoxData,
        DualBoxData,
        ExternalData,
        ListData,
        ValueData
    ]

    def __new__(cls) -> None:
        return None

    @staticmethod
    def init(app: QBaseApplication) -> None:
        BaseItemData.init(app)
        for data in ItemDataFactory._spritedatas:
            data.init(app)
            ItemDataFactory.register(data)

    @staticmethod
    def register(data: type[BaseItemData]) -> None:
        ItemDataFactory._data[data.child_cls.name] = data

    @staticmethod
    def get_data(name: str) -> type[BaseItemData]:
        return ItemDataFactory._data.get(name, BaseItemData)
#----------------------------------------------------------------------
