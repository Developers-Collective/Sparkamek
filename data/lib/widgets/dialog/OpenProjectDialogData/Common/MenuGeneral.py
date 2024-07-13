#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.QtUtils import QLangData, QGridFrame, QNamedLineEdit, QBaseApplication
from .BaseMenu import BaseMenu
#----------------------------------------------------------------------

    # Class
class MenuGeneral(BaseMenu):
    _lang: QLangData = QLangData.NoTranslation()


    @staticmethod
    def init(app: QBaseApplication) -> None:
        MenuGeneral._lang = app.get_lang_data('OpenProjectDialog.QSlidingStackedWidget.general')


    def __init__(self, data: dict) -> None:
        super().__init__()

        lang = self._lang

        self.layout_.setSpacing(30)

        topframe = QGridFrame()
        topframe.layout_.setSpacing(8)
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(topframe, self.layout_.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.layout_.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.layout_.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(root_frame, self.layout_.count(), 0)
        self.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.name.title'), lang.get('QLabel.name.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        self.name_entry = QNamedLineEdit(None, '', lang.get('QNamedLineEdit.name'))
        self.name_entry.setText(data['name'] if data else 'Project')
        root_frame.layout_.addWidget(self.name_entry, root_frame.layout_.count(), 0)
        self.name_entry.text_changed.connect(self.update_continue)


    def update_continue(self, *args, **kwargs) -> None:
        self.can_continue_changed.emit(self.name_entry.text() != '')


    def export(self) -> dict:
        return {
            'name': self.name_entry.text() if self.name_entry.text() else 'Project'
        }
#----------------------------------------------------------------------
