#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class Value(BaseItem):
    name: str = 'value'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.title = data.get_attribute('title', '')
        self.idtype = data.get_attribute('idtype', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self.title} if self.title else {}) |
                ({'idtype': self.idtype} if self.idtype else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )

    def copy(self) -> 'Value':
        return Value(self.export())

    @staticmethod
    def create() -> 'Value':
        return Value(XMLNode('value', attributes = {'nybble': 1, 'title': 'New Value'}))
#----------------------------------------------------------------------
