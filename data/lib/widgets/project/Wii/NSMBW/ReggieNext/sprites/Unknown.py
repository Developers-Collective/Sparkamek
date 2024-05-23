#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class Unknown(BaseItem):
    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self._raw_data = data


    def export(self) -> XMLNode:
        sup = super().export()

        return self._raw_data


    def copy(self) -> 'Unknown':
        return Unknown(self.export())


    @staticmethod
    def create() -> 'Unknown':
        return Unknown(XMLNode(Unknown.name, attributes = {'nybble': 1, 'title': 'New Value'}))
#----------------------------------------------------------------------
