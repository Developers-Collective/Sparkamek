#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from PySide6.QtSvgWidgets import *
from math import *
import os, json, sys
from contextlib import suppress
from datetime import datetime, timedelta
from data.lib import *
#----------------------------------------------------------------------

    # Class
class Application(QBaseApplication):
    SERVER_NAME = Info.application_name
    GITHUB_LINK = Info.github_link

    TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    MESSAGE_DURATION = 5000

    ALERT_RAISE_DURATION = 350
    ALERT_PAUSE_DURATION = 2300
    ALERT_FADE_DURATION = 350

    UPDATE_LINK = Info.github_link

    def __init__(self, platform: QPlatform) -> None:
        super().__init__(platform = platform, app_type = QAppType.Main, single_instance = True)

        self._update_request = None
        self._must_update = False
        self._must_restart = False

        self.setOrganizationName('Synel')
        # self.setApplicationDisplayName(Info.application_name)
        self.setApplicationName(Info.application_name)
        self.setApplicationVersion(Info.version)

        self.another_instance_opened.connect(self.on_another_instance)

        self._save_data = SaveData(
            app = self,
            save_path = Info.save_path,
            main_color_set = Info.main_color_set,
            neutral_color_set = Info.neutral_color_set
        )

        self.save_data.set_stylesheet(self)

        self.setWindowIcon(QIcon(Info.icon_path))

        self.load_colors()

        self.create_widgets()



    def on_another_instance(self) -> None:
        self.window.showMinimized()
        self.window.setWindowState(self.window.windowState() and (not Qt.WindowState.WindowMinimized or Qt.WindowState.WindowActive))



    def load_colors(self) -> None:
        super().load_colors()

        SaveData.COLOR_LINK = self.COLOR_LINK



    def create_widgets(self) -> None:
        self.root = QGridFrame()
        self.root.layout_.setSpacing(0)
        self.root.layout_.setContentsMargins(0, 0, 0, 0)

        self.window.setCentralWidget(self.root)

        pass



    def exit(self) -> None:
        if self._update_request:
            self._update_request.exit()

            if self._update_request.isRunning():
                self._update_request.terminate()

        self.save()

        super().exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    app = Application(QPlatform.Windows)
    app.window.showMaximized()
    sys.exit(app.exec())
#----------------------------------------------------------------------
