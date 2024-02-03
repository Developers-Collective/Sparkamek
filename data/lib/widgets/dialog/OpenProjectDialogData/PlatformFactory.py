#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication
from data.lib.utils import AbstractTypeFactory
from .Platform import Platform
#----------------------------------------------------------------------

    # Class
class PlatformFactory(AbstractTypeFactory):
    _app: QBaseApplication = None


    @staticmethod
    def init(app: QBaseApplication) -> None:
        PlatformFactory._app = app
        Platform.init(app)

        for cls in PlatformFactory()._registry.values():
            cls.init(app)


    @classmethod
    def register(cls_, key: str, cls: type[Platform]) -> None:
        super().register(key, cls)
        if PlatformFactory._app is not None: cls.init(PlatformFactory._app)


    @classmethod
    def create(cls_, key: str, *args, **kwargs) -> Platform:
        return super().create(key, *args, **kwargs)


    @classmethod
    def get(cls, key: str) -> type[Platform]:
        return super().get(key)


    @classmethod
    def get_all(cls) -> tuple[str]:
        return tuple(PlatformFactory()._registry.keys())
#----------------------------------------------------------------------
