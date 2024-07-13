from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineNewWindowRequest
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal


class QTerminalWebEnginePage(QWebEnginePage):
    button_clicked = Signal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._first_load = True


    def acceptNavigationRequest(self, url: QUrl | str, type: QWebEnginePage.NavigationType, is_main_frame: bool) -> bool:
        if self._first_load: return super().acceptNavigationRequest(url, type, is_main_frame)
        return False


    def acceptAsNewWindow(self, request: QWebEngineNewWindowRequest) -> None:
        pass


    def javaScriptConsoleMessage(self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, message: str, line_number: int, source_id: str) -> None:
        if message.startswith('buttonClicked:'):
            button_id = ':'.join(message.split(':')[1:])
            print(button_id)
            self.button_clicked.emit(button_id)
            return
        
        # if level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
        #     print(f'[ERROR] {message} ({source_id}:{line_number})')

        return super().javaScriptConsoleMessage(level, message, line_number, source_id)


    def append_html(self, selector_data: dict, html: str) -> None: # TODO: fix this
        selector = selector_data['selector']

        index = selector_data.get('index', 0)
        if index == 'first': index = 0
        elif index == 'last': index = -1

        html = html.replace('\'', '\\\'')

        # print('\n'.join([
        #     f'var nodes = document.querySelectorAll("{selector}");'.replace('\n', ''),
        #     f'var element = nodes[' + str(index if index >= 0 else f'nodes.length - {index}') + f'];'.replace('\n', ''),
        #     f'element.innerHTML += \'{html}\';'.replace('\n', '')
        # ]))

        self.runJavaScript((
            f'var nodes = document.querySelectorAll("{selector}");'
            f'var element = nodes[' + str(index if index >= 0 else f'nodes.length - {index}') + f'];'
            f'element.innerHTML += \'{html}\';'
        ).replace('\n', ''))
