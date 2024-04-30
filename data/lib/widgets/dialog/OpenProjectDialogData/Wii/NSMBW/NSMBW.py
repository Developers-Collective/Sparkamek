#----------------------------------------------------------------------

    # Libraries
from data.lib.QtUtils import QBaseApplication, QLangData
from .KamekWidget import KamekWidget
from .LoaderWidget import LoaderWidget
from .ReggieNextWidget import ReggieNextWidget
from ..RiivolutionWidget import RiivolutionWidget
from ...GameInfo import GameInfo
from data.lib.widgets.project.ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class NSMBW(GameInfo):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        NSMBW._lang = app.get_lang_data('OpenProjectDialog.game.Wii')
        KamekWidget.init(app)
        LoaderWidget.init(app)
        ReggieNextWidget.init(app)
        RiivolutionWidget.init(app)


    def __init__(self, data: dict) -> None:
        super().__init__()

        self._kamek_widget = KamekWidget(data)
        self._loader_widget = LoaderWidget(data)
        self._reggienext_widget = ReggieNextWidget(data)
        self._riivolution_widget = RiivolutionWidget(data)

        self.add_widget(self._kamek_widget, self._lang.get('NSMBW.kamek.QLabel.title'))
        self.add_widget(self._loader_widget, self._lang.get('NSMBW.loader.QLabel.title'))
        self.add_widget(self._reggienext_widget, self._lang.get('NSMBW.reggieNext.QLabel.title'))
        self.add_widget(self._riivolution_widget, self._lang.get('riivolution.QLabel.title'))


    def export(self) -> dict:
        return {
            'data': {
                ProjectKeys.Wii.NSMBW.Kamek: self._kamek_widget.export(),
                ProjectKeys.Wii.NSMBW.Loader: self._loader_widget.export(),
                ProjectKeys.Wii.NSMBW.ReggieNext: self._reggienext_widget.export(),
                ProjectKeys.Wii.Riivolution: self._riivolution_widget.export()
            }
        }
#----------------------------------------------------------------------
