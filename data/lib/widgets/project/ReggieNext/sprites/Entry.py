#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class Entry(BaseItem):
    name: str = 'entry'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.value = data.get_attribute('value', '')
        self.item = data.value

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'value': self.value} if self.value else {})
            ) | sup.attributes,
            sup.children,
            self.item
        )

    def copy(self) -> 'Entry':
        return Entry(self.export())
#----------------------------------------------------------------------
