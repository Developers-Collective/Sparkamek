#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseSprite import BaseSprite
#----------------------------------------------------------------------

    # Class
class Suggested(BaseSprite):
    name: str = 'suggested'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        sprite = data.get_attribute('sprite')
        self.sprite: int = int(sprite) if sprite != '' and sprite is not None else None

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'sprite': self.sprite} if self.sprite is not None else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        ) if self.sprite is not None else None

    def copy(self) -> 'Suggested':
        return Suggested(self.export())

    @staticmethod
    def create() -> 'Suggested':
        return Suggested(XMLNode('suggested', attributes = {'sprite': 0}))
#----------------------------------------------------------------------
