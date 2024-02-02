#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Option import Option
#----------------------------------------------------------------------

    # Class
class Section(implements(IBaseItem)):
    name: str = 'section'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.name_: str = data.get_attribute('name', 'Section Name') # Required

        self.option_children: list[Option] = [Option(o) for o in data.get_children(Option.name) if o]

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            {'name': self.name_},
            [p.export() for p in self.option_children]
        )

    def copy(self) -> 'Section':
        return Section(self.export())

    @staticmethod
    def create() -> 'Section':
        return Section(XMLNode(Section.name))
#----------------------------------------------------------------------
