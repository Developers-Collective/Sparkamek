#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
#----------------------------------------------------------------------

    # Class
class Suggested(implements(IBaseSprite)):
    name: str = 'suggested'


    def __init__(self, data: XMLNode) -> None:
        sprite = data.get_attribute('sprite')
        self._sprite: int = int(sprite) if sprite != '' and sprite is not None else None


    @property
    def sprite(self) -> int:
        return self._sprite

    @sprite.setter
    def sprite(self, value: int) -> None:
        self._sprite = value


    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'sprite': self._sprite} if self._sprite is not None else {})
            )
        ) if self._sprite is not None else None


    def copy(self) -> 'Suggested':
        return Suggested(self.export())


    @staticmethod
    def create() -> 'Suggested':
        return Suggested(XMLNode('suggested', attributes = {'sprite': 0}))
#----------------------------------------------------------------------
