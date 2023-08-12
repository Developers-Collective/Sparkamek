#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class CheckBox(BaseItem):
    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.title = data.get_attribute('title', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            'checkbox',
            (
                ({'title': self.title} if self.title else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )
#----------------------------------------------------------------------
