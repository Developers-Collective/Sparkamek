#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication, QLangData
from ...GameInfo import GameInfo
from data.lib.widgets.project.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class NSMBU(GameInfo):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        NSMBU._lang = app.get_lang_data('OpenProjectDialog.game.WiiU')
        # TODO: add widgets


    def __init__(self, data: dict) -> None:
        super().__init__()

        # TODO: add widgets


    def export(self) -> dict:
        return {
            'data': {
                # TODO: add widgets
            }
        }
#----------------------------------------------------------------------
