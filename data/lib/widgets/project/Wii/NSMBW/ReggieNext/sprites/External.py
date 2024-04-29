#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
from .ItemFabric import ItemFabric
#----------------------------------------------------------------------

    # Class
class External(BaseItem):
    name: str = 'external'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title = data.get_attribute('title', '')
        self._type = data.get_attribute('type', '')


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value


    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self._title} if self._title else {}) |
                ({'type': self._type} if self._type else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )


    def copy(self) -> 'External':
        return External(self.export())


    @staticmethod
    def create() -> 'External':
        return External(XMLNode(External.name, attributes = {'nybble': 1, 'title': 'New External', 'type': 'actors'}))
#----------------------------------------------------------------------

    # Register Item
ItemFabric.register(External)
#----------------------------------------------------------------------
