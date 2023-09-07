#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils import QBaseApplication, QNamedLineEdit, QSlidingStackedWidget, QGridWidget, QSaveData, QDragList
from ..items.Option import Option
from ..items.Choice import Choice
from .BaseSubItemData import BaseSubItemData
# from .ChoiceData import ChoiceData
#----------------------------------------------------------------------

    # Class
class OptionData(BaseSubItemData):
    type: str = 'Option'
    child_cls: Option = Option

    _add_entry_icon = None
    _back_icon = None

    _lang = {}

    def init(app: QBaseApplication) -> None:
        OptionData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.RiivolutionWidget.WiiDiscWidget.OptionsWidget.SectionData.PropertyWidget.OptionData')

        OptionData._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)
        OptionData._back_icon = app.get_icon('pushbutton/back.png', True, QSaveData.IconMode.Local)

    def __init__(self, data: Option, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._optionname_label = QLabel()
        self._optionname_label.setProperty('brighttitle', True)
        self._content_frame.grid_layout.addWidget(self._optionname_label, 0, 0)

        self._choice_pages = QSlidingStackedWidget()
        self._choice_pages.set_orientation(Qt.Orientation.Horizontal)
        self._property_frame.grid_layout.addWidget(self._choice_pages, 0, 0)


        frame = QGridWidget()
        frame.grid_layout.setSpacing(30)
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._choice_pages.addWidget(frame)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(subframe, 0, 0)

        label = QLabel(self._lang.get_data('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._name_lineedit = QNamedLineEdit(None, '', self._lang.get_data('PropertyWidget.QNamedLineEdit.name'))
        self._name_lineedit.line_edit.setText(self._data.name_)
        self._name_lineedit.line_edit.textChanged.connect(self._name_changed)
        subframe.grid_layout.addWidget(self._name_lineedit, 1, 0)

        subframe.grid_layout.setRowStretch(2, 1)


        subframe = QGridWidget()
        subframe.grid_layout.setSpacing(8)
        subframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(subframe, 1, 0)

        label = QLabel(self._lang.get_data('QLabel.choices'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.grid_layout.addWidget(label, 0, 0)

        self._choice_draglist = QDragList()
        self._choice_draglist.moved.connect(self._choice_entry_moved)
        subframe.grid_layout.addWidget(self._choice_draglist, 1, 0)

        self._add_choice_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_choice_entry_button.setIcon(self._add_entry_icon)
        self._add_choice_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_choice_entry_button.setProperty('color', 'main')
        self._add_choice_entry_button.clicked.connect(self._add_choice_entry)
        subframe.grid_layout.addWidget(self._add_choice_entry_button, 2, 0)
        self._add_choice_entry_button.setEnabled(False)

        subframe.grid_layout.setRowStretch(3, 1)

        frame.grid_layout.setRowStretch(2, 1)


        self._data_frame = QGridWidget()
        self._data_frame.grid_layout.setSpacing(8)
        self._data_frame.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._back_button = QPushButton()
        self._back_button.setIcon(self._back_icon)
        self._back_button.setText(self._lang.get_data('QPushButton.back'))
        self._back_button.setProperty('color', 'main')
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(lambda: self._choice_pages.slide_in_index(0))
        self._data_frame.grid_layout.addWidget(self._back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self._data_frame_content = QGridWidget()
        self._data_frame_content.grid_layout.setSpacing(0)
        self._data_frame_content.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._data_frame.grid_layout.addWidget(self._data_frame_content, 1, 0)

        self._data_frame.grid_layout.setRowStretch(2, 1)

        self._choice_pages.addWidget(self._data_frame)

        self._update_text()

        self._load_data()


    def _load_data(self) -> None:
        self._disable_send = True

        self._choice_draglist.clear()

        self._add_choice_entry_button.setEnabled(self._data is not None)

        if self._data:
            for choice in self._data.choice_children:
                # cd = ChoiceData(choice, self._path)
                # cd.data_changed.connect(self._send_data)
                # cd.edited.connect(self._entry_selected)
                # cd.deleted.connect(self._delete_choice_entry)
                # self._choice_draglist.add_item(cd)
                pass

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get_data('QLabel.text').replace('%s', self._data.name_, 1).replace('%s', str(len(self._data.choice_children)), 1)
        self._optionname_label.setText(s)
        self._name_lineedit.line_edit.setText(self._data.name_)


    def _name_changed(self, text: str) -> None:
        if not text: return

        self._data.name_ = text
        self._update_text()
        self.data_changed.emit()

    def _choice_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.choice_children.insert(new_index, self._data.choice_children.pop(old_index))
        self._send_data()

    def _add_choice_entry(self) -> None:
        c = Choice.create()
        self._data.choice_children.append(c)

        # cd = ChoiceData(c, self._path)
        # cd.data_changed.connect(self._send_data)
        # cd.deleted.connect(self._delete_choice_entry)
        # cd.edited.connect(self._entry_selected)
        # self._choice_draglist.add_item(cd)

        self._send_data()

    # def _delete_choice_entry(self, item: ChoiceData) -> None:
    #     if self._data is None: return

    #     self._data.choice_children.remove(item.data)
    #     item.setParent(None)
    #     item.deleteLater()

    #     self._choice_pages.slide_in_index(0)

    #     self._send_data()

    # def _entry_selected(self, sender: ChoiceData, widget: QGridWidget | None) -> None:
    #     self._set_widget(widget)
    #     self._choice_pages.slide_in_index(1)


    def _set_widget(self, widget: QGridWidget | None) -> None:
        if self._current_widget: self._current_widget.setParent(None)
        if widget: self._data_frame_content.grid_layout.addWidget(widget, 0, 0)
        self._current_widget = widget


    def _send_data(self, *args) -> None:
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
