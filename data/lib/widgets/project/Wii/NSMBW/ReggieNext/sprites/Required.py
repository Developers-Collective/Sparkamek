#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseSprite import IBaseSprite
#----------------------------------------------------------------------

    # Class
class Required(implements(IBaseSprite)):
    name: str = 'required'

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

    def copy(self) -> 'Required':
        return Required(self.export())

    @staticmethod
    def create() -> 'Required':
        return Required(XMLNode('required', attributes = {'sprite': 0}))
#----------------------------------------------------------------------
