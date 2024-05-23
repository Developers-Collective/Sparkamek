#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
from .ItemFabric import ItemFabric
#----------------------------------------------------------------------

    # Class
class HexValue(BaseItem):
    name: str = 'hexvalue'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title = data.get_attribute('title', '')


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self._title} if self._title else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )


    def copy(self) -> 'HexValue':
        return HexValue(self.export())


    @staticmethod
    def create() -> 'HexValue':
        return HexValue(XMLNode(HexValue.name, attributes = {'nybble': 1, 'title': 'New Value'}))
#----------------------------------------------------------------------

    # Register Item
ItemFabric.register(HexValue)
#----------------------------------------------------------------------
