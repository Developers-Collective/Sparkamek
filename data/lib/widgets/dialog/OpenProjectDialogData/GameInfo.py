#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QSidePanelWidget, QSlidingStackedWidget, QBaseApplication, QLangData
#----------------------------------------------------------------------

    # Class
class GameInfo(QSidePanelWidget):
    _lang: QLangData = QLangData.NoTranslation()


    def init(app: QBaseApplication) -> None:
        GameInfo._lang = app.get_lang_data('OpenProjectDialog')


    def __init__(self) -> None:
        super().__init__(None, 200, QSlidingStackedWidget.Direction.Bottom2Top, (16, 16, 16, 16))
#----------------------------------------------------------------------
