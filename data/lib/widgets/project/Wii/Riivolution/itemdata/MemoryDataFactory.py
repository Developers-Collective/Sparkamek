#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from .BaseSubItemData import BaseSubItemData
from .MemoryValueData import MemoryValueData
from .MemoryValueFileData import MemoryValueFileData
from .MemorySearchValueData import MemorySearchValueData
from .MemorySearchValueFileData import MemorySearchValueFileData
from .MemoryOcarinaData import MemoryOcarinaData
#----------------------------------------------------------------------

    # Class
class MemoryDataFactory:
    _app: QBaseApplication = None
    _data: dict[str, BaseSubItemData] = {}

    _memorydatas: list[type[BaseSubItemData]] = [ # Too lazy to make it dynamic
        MemoryValueData,
        MemoryValueFileData,
        MemorySearchValueData,
        MemorySearchValueFileData,
        MemoryOcarinaData,
    ]

    def __new__(cls) -> None:
        return None

    @staticmethod
    def init(app: QBaseApplication) -> None:
        BaseSubItemData.init(app)
        for data in MemoryDataFactory._memorydatas:
            data.init(app)
            MemoryDataFactory.register(data)

    @staticmethod
    def register(data: type[BaseSubItemData]) -> None:
        MemoryDataFactory._data[data.child_cls.key] = data

    @staticmethod
    def get(name: str) -> type[BaseSubItemData]:
        return MemoryDataFactory._data.get(name, BaseSubItemData)

    @staticmethod
    def get_all() -> list[type[BaseSubItemData]]:
        return MemoryDataFactory._data.values()
#----------------------------------------------------------------------
