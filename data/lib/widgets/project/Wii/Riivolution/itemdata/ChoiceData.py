#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QSlidingStackedWidget, QGridWidget, QSaveData, QDragList, QScrollableGridFrame, QLangData
from ..items.Choice import Choice
from ..items.PatchRef import PatchRef
from .BaseSubItemData import BaseSubItemData
from .PatchRefData import PatchRefData
#----------------------------------------------------------------------

    # Class
class ChoiceData(BaseSubItemData):
    type: str = 'Choice'
    child_cls: Choice = Choice

    _add_entry_icon = None
    _back_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        ChoiceData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget.WiiDiscWidget.OptionsWidget.SectionData.PropertyWidget.OptionData.PropertyWidget.ChoiceData')

        ChoiceData._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)
        ChoiceData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

        PatchRefData.init(app)

    def __init__(self, data: Choice, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._optionname_label = QLabel()
        self._optionname_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._optionname_label, 0, 0)

        self._patchref_pages = QSlidingStackedWidget()
        self._patchref_pages.set_orientation(Qt.Orientation.Horizontal)
        self._property_frame.grid_layout.addWidget(self._patchref_pages, 0, 0)


        frame = QScrollableGridFrame()
        frame.set_all_property('transparent', True)
        frame.scroll_layout.setSpacing(30)
        frame.scroll_layout.setContentsMargins(0, 0, 10, 0)

        self._patchref_pages.addWidget(frame)


        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self.back_pressed.emit)
        frame.scroll_layout.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(subframe, 1, 0)

        label = QLabel(self._lang.get('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._name_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.name'))
        self._name_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.name'))
        self._name_lineedit.line_edit.setText(self._data.name_)
        self._name_lineedit.line_edit.textChanged.connect(self._name_changed)
        subframe.grid_layout.addWidget(self._name_lineedit, 1, 0)

        subframe.grid_layout.setRowStretch(2, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.scroll_layout.addWidget(subframe, 2, 0)

        label = QLabel(self._lang.get('QLabel.patches'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._patchref_draglist = QDragList()
        self._patchref_draglist.moved.connect(self._patchref_entry_moved)
        subframe.grid_layout.addWidget(self._patchref_draglist, 1, 0)

        self._add_patchref_entry_button = QPushButton(self._lang.get('QPushButton.addEntry'))
        self._add_patchref_entry_button.setIcon(self._add_entry_icon)
        self._add_patchref_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_patchref_entry_button.setProperty('color', 'main')
        self._add_patchref_entry_button.clicked.connect(self._add_patchref_entry)
        subframe.grid_layout.addWidget(self._add_patchref_entry_button, 2, 0)
        self._add_patchref_entry_button.setEnabled(False)

        subframe.grid_layout.setRowStretch(3, 1)

        frame.scroll_layout.setRowStretch(3, 1)


        self._data_frame = QGridWidget()
        self._data_frame.grid_layout.setSpacing(8)
        self._data_frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._patchref_pages.addWidget(self._data_frame)

        self._update_text()

        self._load_data()


    def _load_data(self) -> None:
        self._disable_send = True

        self._patchref_draglist.clear()

        self._add_patchref_entry_button.setEnabled(self._data is not None)

        if self._data:
            for patchref in self._data.patchref_children:
                prd = PatchRefData(patchref, self._path)
                prd.data_changed.connect(self._send_data)
                prd.deleted.connect(self._delete_patchref_entry)
                self._patchref_draglist.add_item(prd)

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get('QLabel.text').replace('%s', self._data.name_, 1).replace('%s', str(len(self._data.patchref_children)), 1)
        self._optionname_label.setText(s)
        self._name_lineedit.line_edit.setText(self._data.name_)


    def _name_changed(self, text: str) -> None:
        if not text: return

        self._data.name_ = text
        self._update_text()
        self.data_changed.emit()

    def _patchref_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.patchref_children.insert(new_index, self._data.patchref_children.pop(old_index))
        self._send_data()

    def _add_patchref_entry(self) -> None:
        pr = PatchRef.create()
        self._data.patchref_children.append(pr)

        prd = PatchRefData(pr, self._path)
        prd.data_changed.connect(self._send_data)
        prd.deleted.connect(self._delete_patchref_entry)
        self._patchref_draglist.add_item(prd)

        self._send_data()

    def _delete_patchref_entry(self, item: PatchRefData) -> None:
        if self._data is None: return

        self._data.patchref_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._patchref_pages.slide_in_index(0)

        self._send_data()


    def _set_widget(self, widget: QGridWidget | None) -> None:
        if self._current_widget: self._current_widget.setParent(None)
        if widget: self._data_frame.grid_layout.addWidget(widget, 0, 0)
        self._current_widget = widget


    def _send_data(self, *args) -> None:
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
