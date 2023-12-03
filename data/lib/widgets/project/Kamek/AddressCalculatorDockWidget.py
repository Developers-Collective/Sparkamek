#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QPushButton, QLabel
from PySide6.QtCore import Qt, QSortFilterProxyModel
from data.lib.qtUtils import QScrollableGridWidget, QBaseApplication, QSavableDockWidget, QSaveData, QGridWidget, QNamedToggleButton, QUtilsColor, QIconLineEdit, QNamedComboBox, QBetterListWidget, QSlidingStackedWidget, QGridFrame
from .address_calculator import AddressConverterWidget
#----------------------------------------------------------------------

    # Class
class AddressCalculatorDockWidget(QSavableDockWidget):
    _lang = {}

    def init(app: QBaseApplication) -> None:
        AddressCalculatorDockWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.KamekWidget.AddressCalculatorDockWidget')

        AddressConverterWidget.init(app)

    def __init__(self, app: QBaseApplication, name: str, icon: str, data: dict) -> None:
        super().__init__(self._lang.get_data('title').replace('%s', name))

        self._name = name
        self._icon = icon
        self._data = data

        self._root = QGridFrame()
        self._root.setProperty('wide', True)
        self._root.setMinimumWidth(200)
        self._root.setMinimumHeight(100)
        self._root.setFrameShape(QFrame.Shape.NoFrame)
        self._root.setProperty('QDockWidget', True)
        self.setObjectName('addressCalculator')
        self.setWidget(self._root)

        self._sliding_stackwidget = QSlidingStackedWidget()
        self._root.grid_layout.addWidget(self._sliding_stackwidget, 0, 0, Qt.AlignmentFlag.AlignTop)


        self._address_converter_widget = AddressConverterWidget(app, data)
        self._sliding_stackwidget.addWidget(self._address_converter_widget)


    @property
    def task_is_running(self) -> bool:
        return False


    def terminate_task(self) -> None:
        # if self._sprites_and_actors_worker is not None:
        #     self._sprites_and_actors_worker.terminate()
        #     self._sprites_and_actors_worker = None
        pass
#----------------------------------------------------------------------
