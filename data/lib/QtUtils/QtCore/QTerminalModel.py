#----------------------------------------------------------------------

    # Librairies
from .QLangData import QLangData
from .QEnumColor import QEnumColor
from . import QBaseApplication
from ..QtGui.QssParser import QssSelector

import regex
#----------------------------------------------------------------------

    # Class
class QTerminalModel:
    _lang: QLangData = QLangData.NoTranslation()

    _unique_style = '''
        .%name {
            background-color: var(--%name-bg);
        }
        .%name::after {
            border-left-color: var(--%name-bg);
        }
        .%name.special-text:not(.first)::before {
            border-left-color: var(--%name-bg);
        }
'''

    _model: str = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal</title>
</head>
<body>
    <style>
        :root {
            %vars
        }

        * {
            font-family: "Consolas";
            font-size: 1em;

            background-color: var(--bg);
            color: var(--fg);

            /*line-height: 1.5em;*/
        }

        /*html, body {
            max-width: 90%;
            overflow-x: hidden;
        }*/

        body {
            margin: 10px;
            padding: 0;
        }

        body {
            margin-top: 40px;
        }

        div.vertical-space > * {
            margin-top: 0.75em;
        }

        span {
            background-color: transparent;
        }

        .special-text {
            padding-top: 0.125em;
            padding-bottom: 0.188em;
            padding-right: 0.188em;
            padding-left: 0.5em;
            padding-right: 0.25em;
            margin-right: 0.625em;
            color: var(--fg);
            font-weight: bold;
            height: 1.17em;
        }

        .special-text::after {
            content: '';
            position: absolute;
            margin-left: 0.25em;
            margin-top: -0.125em;
            width: 0;
            height: 0;
            border-top: 0.75em solid transparent;
            border-bottom: 0.75em solid transparent;
            border-left: 0.625em solid #000000;
            z-index: 1;
        }

        .special-text.first {
            padding-left: 0.5em;
            border-top-left-radius: 0.625em;
            border-bottom-left-radius: 0.625em;
        }

        .special-text:not(.first)::before {
            content: '';
            position: absolute;
            margin-left: -1.125em;
            width: 0;
            height: 1.49em;
            border-left: 0.65em solid var(--fg);
            margin-top: -0.125em;
        }

        div.columns > div.column {
            margin-right: 0.5em;
        }

        %unique-styles

        div.columns, div.column {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: start;
            min-height: 1.188em;
        }

        a {
            text-decoration: none;
            border: #fff 1px solid;
            padding: 2px 5px;
            border-radius: 10px;
            font-size: 0.775em;
        }
    </style>

    <script>
        function sendButtonClicked(button_id) {
            console.log('buttonClicked:' + button_id);
        }

        document.addEventListener('DOMContentLoaded', function() {
            window.scrollTo(0, document.body.scrollHeight);
        })
    </script>

    <div class="vertical-space">
        %s
    </div>
</body>
</html>
'''

    _app: QBaseApplication = None


    def init(app: QBaseApplication) -> None:
        QTerminalModel._lang = app.get_lang_data('QTerminalModel')
        QTerminalModel._app = app


    def __init__(self, *enum_colors: type[QEnumColor]) -> None:
        self._html = ''
        self._last_added = ''

        fg_color = QTerminalModel._app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QWebEngineView')
        )['color']
        bg_color = QTerminalModel._app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'QTerminalWidget': True}),
            QssSelector(widget = 'QWebEngineView')
        )['background-color']

        root_vars = [
            f'--fg: {fg_color};',
            f'--bg: {bg_color};',
        ]
        unique_styles = []

        for enum_color in enum_colors:
            for color in enum_color:
                root_vars.append(f'--{color.name.lower()}-bg: {color.value.hexa};')
                unique_styles.append(QTerminalModel._unique_style.replace('%name', color.name.lower()))

        self._parsed_model = (
            QTerminalModel._model
                .replace('%vars', '\n'.join(root_vars))
                .replace('%unique-styles', '\n'.join(unique_styles))
        )


    def _str_to_html(self, html: str, accept_empty: bool = True) -> str:
        if html.strip() == '' and not accept_empty:
            return ''

        return (html
            .replace('\r', '')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('&', '&amp;')
            .replace(' ', '&nbsp;')
            .replace('\n', '<br>')
            .replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        )


    def _split_string_around_tags(self, input: str) -> list[str]:
        tag_pattern = regex.compile(r'<[^>]+>')

        split_result = tag_pattern.split(input)

        return split_result


    def _extract_attributes(self, input: str) -> list[tuple[str, tuple[str, ...]]]:
        tag_pattern = regex.compile(r'<(\w+)([^>]*)>')
        attr_pattern = regex.compile(r'(\w+)=["\']?([^"\']+)["\']?')

        results = []

        for tag_match in tag_pattern.finditer(input):
            tag_name = tag_match.group(1)
            attributes_string = tag_match.group(2)

            attributes = tuple(attr_pattern.findall(attributes_string))

            results.append((tag_name, attributes))

        return results


    def _build_element(self, text: str) -> str:
        split = self._split_string_around_tags(text)
        attributes = self._extract_attributes(text)

        for i in range(len(split)):
            split[i] = self._str_to_html(split[i], i >= 0)

            if i % 2 == 0: # Outside a tag
                pass

            else: # Inside a tag
                tag_name, tag_info = attributes[i // 2]

                attr_convert = {}
                attr_disable = {}

                match tag_name:
                    case 'button':
                        tag_name = 'a'
                        attr_convert = {
                            'click': 'onclick="sendButtonClicked(\'%s\')" href="javascript:void(0)"',
                        }

                assembled_attributes = []
                for attr_name, attr_value in tag_info:
                    if attr_name in attr_convert:
                        assembled_attributes.append(attr_convert[attr_name].replace('%s', attr_value))
                        continue

                    if attr_name in attr_disable:
                        continue

                    assembled_attributes.append(f'{attr_name}="{attr_value}"')

                assembled_attributes = ' '.join(assembled_attributes)

                split[i] = f'<{tag_name} {assembled_attributes}>{split[i]}</{tag_name}>'

        return ''.join(split)


    def log_empty(self, *args, **kwargs) -> str:
        div = f'<div class="columns"></div>'
        self._html += self._last_added + div
        self._last_added = ''

        return div


    def log(self, text: str, *log_types: QEnumColor, continuous: bool = False) -> str:
        if not log_types or not (text.strip()):
            self.log_empty()

        div = f'<div class="columns">%s</div>'

        if continuous:
            add = self._build_element(text)

            last_span = self._last_added.rfind('</span>')
            if last_span != -1:
                self._last_added = self._last_added[:last_span] + '<br>' + add + self._last_added[last_span:]
            else: self._last_added += add

            return add

        parts = (
            f'<div class="column">' + ''.join((
                f'<span class="special-text{" first" if i == 0 else ""} {log_type.name.lower()}">'
                    f'{self._lang.get(log_type.name.lower())}'
                f'</span>'
            ) for i, log_type in enumerate(log_types)) + '</div>',
            f'<span>{self._build_element(text)}</span>'
        )

        self._html += self._last_added
        self._last_added = div.replace('%s', '\n'.join(parts))

        return self._last_added


    def render(self) -> str:
        return self._parsed_model.replace('%s', self._html + self._last_added)


    def clear(self) -> None:
        self._html = ''
        self._last_added = ''
#----------------------------------------------------------------------
