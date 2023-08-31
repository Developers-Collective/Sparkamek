#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Region import Region
#----------------------------------------------------------------------

    # Class
class Network(implements(IBaseItem)):
    name: str = 'network'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.protocol: str = data.get_attribute('protocol', 'riifs') # Required
        self.address: str = data.get_attribute('address', '127.0.0.1') # Required
        self.port: int = int(data.get_attribute('port', 1137)) # Required

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'protocol': self.protocol} |
                {'address': self.address} |
                {'port': self.port}
            )
        )

    def copy(self) -> 'Network':
        return Network(self.export())

    @staticmethod
    def create() -> 'Network':
        return Network(XMLNode(Network.name))
#----------------------------------------------------------------------
