#----------------------------------------------------------------------

    # Libraries
from data.lib.utils.AbstractTypeFactory import AbstractTypeFactory
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class ItemFabric(AbstractTypeFactory):
    @classmethod
    def register(cls_, cls: type[BaseItem]) -> None:
        return super().register(cls.name, cls)


    @classmethod
    def create(cls_, data: XMLNode) -> BaseItem:
        return super().create(data.name, data)


    @classmethod
    def get(cls_, key: str) -> type[BaseItem]:
        return super().get(key)
#----------------------------------------------------------------------
