#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
from .Entry import Entry
#----------------------------------------------------------------------

    # Class
class List(BaseItem):
    name: str = 'list'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title = data.get_attribute('title', '')
        self._children = [Entry(e) for e in data.get_children('entry')]


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value


    @property
    def children(self) -> list[Entry]:
        return self._children


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self._title} if self._title else {})
            ) | sup.attributes,
            sup.children + [e.export() for e in self._children],
            sup.value
        )


    def copy(self) -> 'List':
        return List(self.export())


    @staticmethod
    def create() -> 'List':
        return List(XMLNode('list', attributes = {'nybble': 1, 'title': 'New List'}))
#----------------------------------------------------------------------
