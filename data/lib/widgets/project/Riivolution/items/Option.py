#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Choice import Choice
#----------------------------------------------------------------------

    # Class
class Option(implements(IBaseItem)):
    name: str = 'option'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.id: str = data.get_attribute('id', '') # Optional
        self.name_: str = data.get_attribute('name', 'Option Name') # Required
        self.default: int = int(data.get_attribute('default', 0)) # Optional

        self.choice_children: list[Choice] = [Choice(c) for c in data.get_children(Choice.name) if c]

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'id': self.id} if self.id else {}) |
                {'name': self.name_} |
                ({'default': self.default} if self.default != None else {})
            ),
            [p.export() for p in self.choice_children]
        )

    def copy(self) -> 'Option':
        return Option(self.export())

    @staticmethod
    def create() -> 'Option':
        return Option(XMLNode(Option.name))
#----------------------------------------------------------------------
