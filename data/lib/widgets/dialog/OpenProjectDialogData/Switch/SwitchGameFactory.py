#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication
from data.lib.utils import AbstractTypeFactory
from ..Game import Game
#----------------------------------------------------------------------

    # Class
class SwitchGameFactory(AbstractTypeFactory):
    _app: QBaseApplication = None


    @staticmethod
    def init(app: QBaseApplication) -> None:
        SwitchGameFactory._app = app

        for cls in SwitchGameFactory()._registry.values():
            cls.init(app)


    @classmethod
    def register(cls_, key: str, cls: type[Game]) -> None:
        super().register(key, cls)
        if SwitchGameFactory._app is not None: cls.init(SwitchGameFactory._app)


    @classmethod
    def create(cls_, key: str, *args, **kwargs) -> Game:
        return super().create(key, *args, **kwargs)


    @classmethod
    def get(cls, key: str) -> type[Game]:
        return super().get(key)


    @classmethod
    def get_all(cls) -> tuple[str]:
        return tuple(SwitchGameFactory()._registry.keys())
#----------------------------------------------------------------------
