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
        self.sprite: int = int(sprite) if sprite != '' and sprite is not None else None

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'sprite': self.sprite} if self.sprite is not None else {})
            )
        ) if self.sprite is not None else None

    def copy(self) -> 'Suggested':
        return Suggested(self.export())

    @staticmethod
    def create() -> 'Suggested':
        return Suggested(XMLNode('suggested', attributes = {'sprite': 0}))
#----------------------------------------------------------------------
