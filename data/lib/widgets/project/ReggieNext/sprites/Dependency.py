#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
from .Suggested import Suggested
from .Required import Required
#----------------------------------------------------------------------

    # Class
class Dependency(implements(IBaseSprite)):
    name: str = 'dependency'

    def __init__(self, data: XMLNode) -> None:
        self._suggested = [Suggested(s) for s in data.get_children('suggested')]
        self.required = [Required(r) for r in data.get_children('required')]

        self.notes: str = data.get_attribute('notes', '')

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'notes': self.notes} if self.notes else {})
            ),
            [s.export() for s in self._suggested if s.export()] + [r.export() for r in self.required if r.export()]
        ) if self._suggested or self.required else None

    def copy(self) -> 'Dependency':
        return Dependency(self.export())

    @staticmethod
    def create() -> 'Dependency':
        return Dependency(XMLNode('dependency'))
#----------------------------------------------------------------------
