#----------------------------------------------------------------------

    # Libraries
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QLangData
from ..items.PatchRef import PatchRef
from .BaseItemData import BaseItemData
#----------------------------------------------------------------------

    # Class
class PatchRefData(BaseItemData):
    type: str = 'PatchRef'
    child_cls: PatchRef = PatchRef

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        PatchRefData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.OptionsWidget.SectionData.PropertyWidget.OptionData.PropertyWidget.ChoiceData.PropertyWidget.PatchRefData')

    def __init__(self, data: PatchRef, path: str) -> None:
        super().__init__(data, path)

        self.setProperty('checkable', False)
        self.setProperty('bottom-border-only', False)

        self._current_widget = None

        self._id_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.id'))
        self._id_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.id'))
        self._id_lineedit.line_edit.setText(self._data.id)
        self._id_lineedit.line_edit.textChanged.connect(self._id_changed)
        self._content_frame.grid_layout.addWidget(self._id_lineedit, 0, 0)


    def _id_changed(self, text: str) -> None:
        if not text: return

        self._data.id = text
        self._send_data()


    def _send_data(self, *args) -> None:
        self.data_changed.emit()

    def set_checked(self, checked: bool) -> None:
        super().set_checked(False)
#----------------------------------------------------------------------
