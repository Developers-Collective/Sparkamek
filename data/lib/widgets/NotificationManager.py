#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from data.lib.utils import AbstractFactory
#----------------------------------------------------------------------

    # Class
class NotificationManager(AbstractFactory):
    _app: QBaseApplication = None


    @classmethod
    def register(cls, key: str, data: dict) -> None:
        if key in cls()._registry: return
        super().register(key, data)


    @classmethod
    def get(cls, key: str) -> dict:
        return super().get(key)


    @classmethod
    def get_all(cls) -> tuple[str]:
        return tuple(NotificationManager()._registry.keys())
#----------------------------------------------------------------------
