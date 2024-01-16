#----------------------------------------------------------------------

    # Libraries
import json, os
from typing import Union
#----------------------------------------------------------------------

    # Class
class QLangData:
    class NoTranslation:
        def __getitem__(self, __key: str) -> 'QLangData.NoTranslation':
            return self


        def __getattr__(self, __key: str) -> 'QLangData.NoTranslation':
            return self


        def get(self, *args, **kwargs) -> 'QLangData.NoTranslation':
            return self


        def __call__(self, *args, **kwargs) -> 'QLangData.NoTranslation':
            return self


        def __str__(self) -> str:
            return 'No translation available'


        def __repr__(self) -> str:
            return str(self)



    def __init__(self, data: dict = {}, cwd: str = './', current_file: str = '???') -> None:
        self._current_file = current_file

        self._data = {}

        for key, value in data.items():
            if isinstance(value, dict):
                self._data[key] = QLangData(value, cwd, current_file)
                continue

            if isinstance(value, str):
                if value.startswith('#ref:'):
                    file = value.replace('#ref:', '').replace(' ', '').replace('\\', '/')

                    if not os.path.exists(f'{cwd}{file}.json'): raise Exception(f'Cannot find {cwd}{file}.json')
                    with open(f'{cwd}{file}.json', 'r', encoding = 'utf-8') as infile:
                        try:
                            self._data[key] = QLangData(json.load(infile), cwd, f'{cwd}{file}.json')

                        except Exception as e:
                            raise Exception(f'Error in {cwd}{file}.json:\n{e}')

                    continue

            self._data[key] = value


    def get(self, path: str, default: Union[str, 'QLangData', None] = None) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        keys = path.split('.')
        data = self

        for key in keys:
            try: data = data[key]
            except KeyError as e: raise Exception(f'Cannot find {e.args[0]} of {path} in {self._current_file}')

        if default is not None and isinstance(data, self.NoTranslation): return default
        return data


    def __getattr__(self, key: str) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        try: return self._data[key]
        except KeyError: return self.NoTranslation()


    def __getitem__(self, key: str) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        try: return self._data[key]
        except KeyError: return self.NoTranslation()


    def __call__(self, *args, **kwargs) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        return self
#----------------------------------------------------------------------
