#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication, QLangData, QSidePanelWidget
from .KamekWidget import KamekWidget
from .LoaderWidget import LoaderWidget
from .ReggieNextWidget import ReggieNextWidget
from ..RiivolutionWidget import RiivolutionWidget
from ...WidgetFactory import WidgetFactory
#----------------------------------------------------------------------

    # Class
class NSMBW(QSidePanelWidget):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        NSMBW._lang = app.get_lang_data('OpenProjectDialog.Wii.NSMBW')
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

        self.add_widget(self._kamek_widget, self._lang.get('QSidePanelWidget.kamek'))
        self.add_widget(self._loader_widget, self._lang.get('QSidePanelWidget.loader'))
        self.add_widget(self._reggienext_widget, self._lang.get('QSidePanelWidget.reggienext'))
        self.add_widget(self._riivolution_widget, self._lang.get('QSidePanelWidget.riivolution'))
#----------------------------------------------------------------------

    # Setup
WidgetFactory.register('Wii.NSMBW', NSMBW)
#----------------------------------------------------------------------
