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

        self._value = int(data.get_attribute('value', '0'))
        self._item = data.value

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'value': self._value} if self._value is not None else {})
            ) | sup.attributes,
            sup.children,
            self._item
        )

    def copy(self) -> 'Entry':
        return Entry(self.export())

    @staticmethod
    def create() -> 'Entry':
        return Entry(XMLNode('entry', attributes = {'nybble': 1, 'value': 0}, value = 'New Entry'))
#----------------------------------------------------------------------
