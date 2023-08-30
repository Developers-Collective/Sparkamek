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

        self.name: str = data.get_attribute('name', 'Section Name') # Required

        self.option_children: list[Option] = data.get_children(Option.name)

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            {'name': self.name},
            [p.export() for p in self.option_children]
        )

    def copy(self) -> 'Section':
        return Section(self.export())

    @staticmethod
    def create() -> 'Section':
        return Section(XMLNode(Section.name))
#----------------------------------------------------------------------
