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

        self._value = int(data.get_attribute('value', '0'))
        self._item = data.value


    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value


    @property
    def item(self) -> int:
        return self._item

    @item.setter
    def item(self, value: int) -> None:
        self._item = value


    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'value': self._value} if self._value is not None else {})
            ),
            [],
            self._item
        )


    def copy(self) -> 'Entry':
        return Entry(self.export())


    @staticmethod
    def create() -> 'Entry':
        return Entry(XMLNode('entry', value = 'New Entry'))
#----------------------------------------------------------------------
