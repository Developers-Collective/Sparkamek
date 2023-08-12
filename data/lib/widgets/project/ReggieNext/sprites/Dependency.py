#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseSprite import BaseSprite
from .Suggested import Suggested
from .Required import Required
#----------------------------------------------------------------------

    # Class
class Dependency(BaseSprite):
    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.suggested = [Suggested(s) for s in data.get_children('suggested')]
        self.required = [Required(r) for r in data.get_children('required')]

        self.notes: str = data.get_attribute('notes', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            'dependency',
            (
                ({'notes': self.notes} if self.notes else {})
            ) | sup.attributes,
            sup.children + [s.export() for s in self.suggested if s.export()] + [r.export() for r in self.required if r.export()],
            sup.value
        )
#----------------------------------------------------------------------
