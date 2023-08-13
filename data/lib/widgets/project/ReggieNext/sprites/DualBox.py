#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class DualBox(BaseItem):
    name: str = 'dualbox'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.title1 = data.get_attribute('title1', '')
        self.title2 = data.get_attribute('title2', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title1': self.title1} if self.title1 else {}) |
                ({'title2': self.title2} if self.title2 else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )

    def copy(self) -> 'DualBox':
        return DualBox(self.export())
#----------------------------------------------------------------------
