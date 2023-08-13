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

        self.title = data.get_attribute('title', '')
        self.children = [Entry(e) for e in data.get_children('entry')]

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self.title} if self.title else {})
            ) | sup.attributes,
            sup.children + [e.export() for e in self.children],
            sup.value
        )

    def copy(self) -> 'List':
        return List(self.export())
#----------------------------------------------------------------------
