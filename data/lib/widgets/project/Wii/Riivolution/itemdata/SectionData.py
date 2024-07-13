#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from data.lib.QtUtils import QBaseApplication, QNamedLineEdit, QSlidingStackedWidget, QGridWidget, QSaveData, QDragList, QScrollableGridFrame, QLangData
from ..items.Section import Section
from ..items.Option import Option
from .BaseItemData import BaseItemData
from .OptionData import OptionData
#----------------------------------------------------------------------

    # Class
class SectionData(BaseItemData):
    type: str = 'Section'
    child_cls: Section = Section

    _add_entry_icon = None

    _lang: QLangData = QLangData.NoTranslation()

    def init(app: QBaseApplication) -> None:
        SectionData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.RiivolutionWidget.WiiDiscWidget.OptionsWidget.SectionData')

        SectionData._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        OptionData.init(app)

    def __init__(self, data: Section, path: str) -> None:
        super().__init__(data, path)

        self._disable_send = False
        self._current_widget = None

        self._sectionname_label = QLabel()
        self._sectionname_label.setProperty('brighttitle', True)
        self._content_frame.layout_.addWidget(self._sectionname_label, 0, 0)

        self._option_pages = QSlidingStackedWidget()
        self._option_pages.set_orientation(Qt.Orientation.Horizontal)
        self._property_frame.layout_.addWidget(self._option_pages, 0, 0)


        frame = QScrollableGridFrame()
        frame.set_all_property('transparent', True)
        frame.layout_.setSpacing(30)
        frame.layout_.setContentsMargins(0, 0, 10, 0)

        self._option_pages.addWidget(frame)


        subframe = QGridWidget()
        subframe.layout_.setSpacing(8)
        subframe.layout_.setContentsMargins(0, 0, 0, 0)
        frame.layout_.addWidget(subframe, 0, 0)

        label = QLabel(self._lang.get('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.layout_.addWidget(label, 0, 0)

        self._name_lineedit = QNamedLineEdit(None, '', self._lang.get('PropertyWidget.QNamedLineEdit.name'))
        self._name_lineedit.setToolTip(self._lang.get('PropertyWidget.QToolTip.name'))
        self._name_lineedit.line_edit.setText(self._data.name_)
        self._name_lineedit.line_edit.textChanged.connect(self._name_changed)
        subframe.layout_.addWidget(self._name_lineedit, 1, 0)

        subframe.layout_.setRowStretch(2, 1)


        subframe = QGridWidget()
        subframe.layout_.setSpacing(8)
        subframe.layout_.setContentsMargins(0, 0, 0, 0)
        frame.layout_.addWidget(subframe, 1, 0)

        label = QLabel(self._lang.get('QLabel.options'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        subframe.layout_.addWidget(label, 0, 0)

        self._option_draglist = QDragList()
        self._option_draglist.moved.connect(self._option_entry_moved)
        subframe.layout_.addWidget(self._option_draglist, 1, 0)

        self._add_option_entry_button = QPushButton(self._lang.get('QPushButton.addEntry'))
        self._add_option_entry_button.setIcon(self._add_entry_icon)
        self._add_option_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_option_entry_button.setProperty('color', 'main')
        self._add_option_entry_button.clicked.connect(self._add_option_entry)
        subframe.layout_.addWidget(self._add_option_entry_button, 2, 0)
        self._add_option_entry_button.setEnabled(False)

        subframe.layout_.setRowStretch(3, 1)

        frame.layout_.setRowStretch(2, 1)


        self._data_frame = QGridWidget()
        self._data_frame.layout_.setSpacing(8)
        self._data_frame.layout_.setContentsMargins(0, 0, 0, 0)

        self._option_pages.addWidget(self._data_frame)

        self._update_text()

        self._load_data()


    def _load_data(self) -> None:
        self._disable_send = True

        self._option_draglist.clear()

        self._add_option_entry_button.setEnabled(self._data is not None)

        if self._data:
            for option in self._data.option_children:
                od = OptionData(option, self._path)
                od.data_changed.connect(self._send_data)
                od.edited.connect(self._entry_selected)
                od.deleted.connect(self._delete_option_entry)
                self._option_draglist.add_item(od)
                pass

        self._disable_send = False


    def _update_text(self) -> None:
        s = self._lang.get('QLabel.text').replace('%s', self._data.name_, 1).replace('%s', str(len(self._data.option_children)), 1)
        self._sectionname_label.setText(s)
        self._name_lineedit.line_edit.setText(self._data.name_)


    def _name_changed(self, text: str) -> None:
        if not text: return

        self._data.name_ = text
        self._update_text()
        self.data_changed.emit()

    def _option_entry_moved(self, old_index: int, new_index: int) -> None:
        self._data.option_children.insert(new_index, self._data.option_children.pop(old_index))
        self._send_data()

    def _add_option_entry(self) -> None:
        s = Option.create()
        self._data.option_children.append(s)

        od = OptionData(s, self._path)
        od.data_changed.connect(self._send_data)
        od.deleted.connect(self._delete_option_entry)
        od.edited.connect(self._entry_selected)
        self._option_draglist.add_item(od)

        self._send_data()

    def _delete_option_entry(self, item: OptionData) -> None:
        if self._data is None: return

        self._data.option_children.remove(item.data)
        item.setParent(None)
        item.deleteLater()

        self._option_pages.slide_in_index(0)

        self._send_data()

    def _entry_selected(self, sender: OptionData, widget: QGridWidget | None) -> None:
        self._set_widget(widget)
        try: sender.back_pressed.disconnect()
        except: pass
        sender.back_pressed.connect(lambda: self._option_pages.slide_in_index(0))
        self._option_pages.slide_in_index(1)


    def _set_widget(self, widget: QGridWidget | None) -> None:
        if self._current_widget: self._current_widget.setParent(None)
        if widget: self._data_frame.layout_.addWidget(widget, 0, 0)
        self._current_widget = widget


    def _send_data(self, *args) -> None:
        self._update_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
