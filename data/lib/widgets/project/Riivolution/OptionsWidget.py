#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QLangData
from data.lib.widgets.project.ProjectKeys import ProjectKeys
from .items import Options, Section
from .itemdata import SectionData
#----------------------------------------------------------------------

    # Class
class OptionsWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.Wii.SME.ReggieNext

    data_changed = Signal()
    property_entry_selected = Signal(QGridWidget or None)

    _app: QBaseApplication = None

    _add_entry_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        OptionsWidget._app = app

        OptionsWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.OptionsWidget')
        OptionsWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        SectionData.init(app)

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path

        self._disable_send = True

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)


        frame = QGridWidget()
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(frame, 0, 0)

        label = QLabel(self._lang.get('QLabel.options'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        frame.grid_layout.addWidget(label, 2, 0)

        self._section_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._section_draglist.moved.connect(self._section_entry_moved)
        frame.grid_layout.addWidget(self._section_draglist, 3, 0)

        self._add_section_entry_button = QPushButton(self._lang.get('QPushButton.addEntry'))
        self._add_section_entry_button.setIcon(self._add_entry_icon)
        self._add_section_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_section_entry_button.setProperty('color', 'main')
        self._add_section_entry_button.clicked.connect(self._add_section_entry)
        frame.grid_layout.addWidget(self._add_section_entry_button, 4, 0)
        self._add_section_entry_button.setEnabled(False)


        self._options: Options = None


    @property
    def options(self) -> Options:
        return self._options

    @options.setter
    def options(self, options: Options) -> None:
        self._options = options

        self._disable_send = True

        self._section_draglist.clear()

        self._add_section_entry_button.setEnabled(self._options is not None)

        if self._options:
            for section in self._options.section_children:
                sd = SectionData(section, self._path)
                sd.data_changed.connect(self._send_data)
                sd.selected.connect(self._entry_selected)
                sd.deleted.connect(self._delete_section_entry)
                self._section_draglist.add_item(sd)

        self._disable_send = False


    def _section_entry_moved(self, old_index: int, new_index: int) -> None:
        self._options.section_children.insert(new_index, self._options.section_children.pop(old_index))
        self._send_data()

    def _add_section_entry(self) -> None:
        s = Section.create()
        self._options.section_children.append(s)

        sd = SectionData(s, self._path)
        sd.data_changed.connect(self._send_data)
        sd.deleted.connect(self._delete_section_entry)
        sd.selected.connect(self._entry_selected)
        self._section_draglist.add_item(sd)

        self._send_data()

    def _delete_section_entry(self, item: SectionData) -> None:
        if self._options is None: return

        self._options.section_children.remove(item.data)
        item.deleteLater()

        self.property_entry_selected.emit(None)

        for item in self._section_draglist.items:
            item.set_checked(False)

        self._send_data()

    def _entry_selected(self, sender: SectionData, widget: QGridWidget | None) -> None:
        checked = sender.is_checked()

        self.deselect_all()

        sender.set_checked(checked)
        self.property_entry_selected.emit(widget)

    def deselect_all(self) -> None:
        self._disable_send = True

        for item in self._section_draglist.items:
            item.set_checked(False)

        self._disable_send = False


    def _send_data(self, *args) -> None:
        self.data_changed.emit()


    def _name_changed(self, text: str) -> None:
        if self._disable_send: return

        self._options.name = text
        self._send_data()
#----------------------------------------------------------------------
