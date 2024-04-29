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
        self._required = [Required(r) for r in data.get_children('required')]

        self._notes: str = data.get_attribute('notes', '')


    @property
    def suggested(self) -> list[Suggested]:
        return self._suggested


    @property
    def required(self) -> list[Required]:
        return self._required


    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        self._notes = value


    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'notes': self._notes} if self._notes else {})
            ),
            [s.export() for s in self._suggested if s.export()] + [r.export() for r in self._required if r.export()]
        ) if self._suggested or self._required else None


    def copy(self) -> 'Dependency':
        return Dependency(self.export())


    @staticmethod
    def create() -> 'Dependency':
        return Dependency(XMLNode(Dependency.name))
#----------------------------------------------------------------------
