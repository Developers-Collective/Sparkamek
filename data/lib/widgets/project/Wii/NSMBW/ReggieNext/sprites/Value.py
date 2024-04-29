#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
from .ItemFabric import ItemFabric
#----------------------------------------------------------------------

    # Class
class Value(BaseItem):
    name: str = 'value'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title = data.get_attribute('title', '')
        self._idtype = data.get_attribute('idtype', '')


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value


    @property
    def idtype(self) -> str:
        return self._idtype

    @idtype.setter
    def idtype(self, value: str) -> None:
        self._idtype = value


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self._title} if self._title else {}) |
                ({'idtype': self._idtype} if self._idtype else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )


    def copy(self) -> 'Value':
        return Value(self.export())


    @staticmethod
    def create() -> 'Value':
        return Value(XMLNode(Value.name, attributes = {'nybble': 1, 'title': 'New Value'}))
#----------------------------------------------------------------------

    # Register Item
ItemFabric.register(Value)
#----------------------------------------------------------------------
