#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XML
from .Sprite import Sprite
#----------------------------------------------------------------------

    # Class
class Sprites:
    def __init__(self, data: XML = None) -> None:
        if data: self.children = [Sprite(c) for c in data.children]
        else: self.children = []

    def __getitem__(self, index: int) -> Sprite:
        return self.children[index]
    
    def __len__(self) -> int:
        return len(self.children)
    
    def __iter__(self) -> Sprite:
        return iter(self.children)
    
    def get(self, id: int) -> Sprite:
        return self.children[id]

    def get_by_id(self, id: int) -> Sprite:
        sprite = next((s for s in self.children if s.id == id), None)
        if sprite is None: raise ValueError(f'Sprite ID not found: {id}')
        return sprite

    def add(self, sprite: Sprite) -> None:
        if sprite.id is None: raise ValueError('Sprite ID cannot be None')
        if sprite.id in [s.id for s in self.children]: raise ValueError(f'Sprite ID already exists: {sprite.id}')
        self.children.append(sprite)

    def remove(self, sprite: Sprite | int) -> None:
        if isinstance(sprite, int): self.children.pop(sprite)
        else: self.children.remove(sprite)

    def remove_by_id(self, id: str) -> None:
        self.remove(self.get_by_id(id))

    def export(self) -> XML:
        return XML(
            'sprites',
            [c.export() for c in self.children]
        )
#----------------------------------------------------------------------
