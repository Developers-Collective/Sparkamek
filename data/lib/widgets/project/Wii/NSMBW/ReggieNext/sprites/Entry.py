#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
#----------------------------------------------------------------------

    # Class
class Entry(implements(IBaseSprite)):
    name: str = 'entry'

    def __init__(self, data: XMLNode) -> None:
        super().__init__()

        self.value = int(data.get_attribute('value', '0'))
        self.item = data.value

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'value': self.value} if self.value is not None else {})
            ),
            [],
            self.item
        )

    def copy(self) -> 'Entry':
        return Entry(self.export())

    @staticmethod
    def create() -> 'Entry':
        return Entry(XMLNode('entry', value = 'New Entry'))
#----------------------------------------------------------------------
