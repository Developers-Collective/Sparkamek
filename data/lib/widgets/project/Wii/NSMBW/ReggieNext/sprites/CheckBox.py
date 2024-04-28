#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from data.lib.widgets.project.Wii.NSMBW.ReggieNext.sprites.BaseItem import BaseItem
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class CheckBox(BaseItem):
    name: str = 'checkbox'


    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._title = data.get_attribute('title', '')


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value


    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self._title} if self._title else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )


    def copy(self) -> 'CheckBox':
        return CheckBox(self.export())


    @staticmethod
    def create() -> 'CheckBox':
        return CheckBox(XMLNode('checkbox', attributes = {'nybble': 1, 'title': 'New Checkbox'}))
#----------------------------------------------------------------------
