#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication, QLangData
from ...GameInfo import GameInfo
from data.lib.widgets.project.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class SMBWonder(GameInfo):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        SMBWonder._lang = app.get_lang_data('OpenProjectDialog.game.Switch')
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
