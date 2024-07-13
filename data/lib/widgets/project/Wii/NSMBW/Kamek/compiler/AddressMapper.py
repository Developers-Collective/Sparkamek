#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QObject
import dataclasses, typing, re, yaml, os

from data.lib.QtUtils import QLogsColor
from .....ProjectException import ProjectException
from .KamekConstants import KamekConstants
#----------------------------------------------------------------------

    # Class
class AddressMapper(QObject):
    @dataclasses.dataclass
    class Mapping:
        start: int = None
        end: int = None
        delta: int = None

        def overlaps(self, other: 'AddressMapper.Mapping'):
            return (self.end >= other.start) and (self.start <= other.end)

        def __str__(self):
            return f'{self.start:08X}-{self.end:08X}: {"+" if self.delta >= 0 else "-"}0x{abs(self.delta)}'

        def __repr__(self):
            return f'<mapping {self!s}>'


    # base: 'AddressMapper' = None

    def __init__(self, name: str, version: str, base: 'AddressMapper' = None) -> None:
        super(AddressMapper, self).__init__()
        self._name = name
        self._version = version
        self._mappings: list[AddressMapper.Mapping] = []
        self._base: AddressMapper = base


    @property
    def name(self) -> str:
        return self._name


    @property
    def version(self) -> str:
        return self._version


    @property
    def base(self) -> 'AddressMapper':
        return self._base
    
    @base.setter
    def base(self, value: 'AddressMapper') -> None:
        self._base = value


    def add_mapping(self, start: int, end: int, delta: int) -> None:
        if start > end:
            raise ValueError(f'cannot map {start:08X}-{end:08X} as start is higher than end')

        new_mapping = self.Mapping(start, end, delta)

        for mapping in self._mappings:
            if mapping.overlaps(new_mapping):
                raise ValueError(f'mapping "{new_mapping}" overlaps with earlier mapping "{mapping}"')

        self._mappings.append(new_mapping)


    def remap(self, input: int) -> int:
        if self.base is not None:
            input = self.base.remap(input)

        for mapping in self._mappings:
            if mapping.start <= input <= mapping.end:
                # print(f'[REMAP] {mapping.start:X}-{mapping.end:X}: {mapping.delta:X} => {input:X} => {input + mapping.delta:X}')
                return input + mapping.delta

        return input


    def demap(self, input: int) -> int:
        for mapping in self._mappings:
            if (mapping.start + mapping.delta) <= input <= (mapping.end + mapping.delta):
                input = input - mapping.delta
                break

        if self.base is not None:
            input = self.base.demap(input)

        return input


    def demap_reverse(self, input: int) -> int:
        for mapping in self._mappings:
            if mapping.start <= input <= mapping.end:
                # print(f'[DEMAP] {mapping.start:X}-{mapping.end:X}: {mapping.delta:X} => {input:X} => {input + mapping.delta:X}')
                input = input + mapping.delta
                break

        if self.base is not None:
            input = self.base.demap_reverse(input)

        return input


    def items(self) -> list[Mapping]:
        return self._mappings.copy()


    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self._mappings])


    def inherits_from(self, other: 'AddressMapper | str | None') -> bool:
        if other == 'unk': return False

        if isinstance(other, AddressMapper) and self.base == other:
            return True

        if isinstance(other, str) and self.base and self.base.name == other:
            return True

        return self.base.inherits_from(other) if self.base else False


    def is_or_inherits_from(self, other: 'AddressMapper | str | None') -> bool:
        if isinstance(other, AddressMapper) and self == other:
            return True

        if isinstance(other, str) and self.name == other:
            return True

        return self.inherits_from(other)



class AddressMapperController(QObject):
    log_simple = Signal(str, QLogsColor, bool, tuple)
    log_complete = Signal(str, QLogsColor, bool, tuple)

    def __init__(self, cwd: str, project_path: str, base_version: str, version_ids: dict) -> None:
        super(AddressMapperController, self).__init__()

        self._project_path = project_path
        self._cwd = cwd

        self._base_version = base_version
        self._version_ids = version_ids
        self._reverse_version_ids = {v: k for k, v in version_ids.items()}


    @property
    def _project_full_path(self) -> str:
        return f'{self._cwd}/{self._project_path}'


    def run(self) -> None:
        path = KamekConstants.get_versions_nsmbw(self._cwd)
        
        if not os.path.exists(path):
            raise ProjectException(f'Unable to find "<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">versions-nsmbw.txt</span>" at "{self._cwd}/tools"', QLogsColor.Error)

        with open(path, 'r', encoding = 'utf-8') as infile:
            try: mappers = AddressMapperController.read_version_info(infile, self._reverse_version_ids)
            except ValueError as e: raise ProjectException(str(e), QLogsColor.Error)
            except ProjectException as e: raise e

        if not os.path.isdir(f'{self._cwd}/processed'):
            os.mkdir(f'{self._cwd}/processed')

        for x_id, txt_id in self._version_ids.items():
            try: self._do_mapfile(f'kamek_{self._base_version}.x', f'kamek_{x_id}.x', mappers[txt_id])
            except FileNotFoundError: raise ProjectException(f'Unable to find "<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">kamek_{self._base_version}.x</span>" at "{self._cwd}"', QLogsColor.Error)
            except KeyError: raise ProjectException(f'Unable to find version <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{txt_id}</span> in {self._cwd}/tools/versions-nsmbw.txt', QLogsColor.Error)
            except Exception as e: raise ProjectException(str(e), QLogsColor.Error)

        already_done = set()
        try: self._do_project(self._project_full_path, already_done, mappers)
        except FileNotFoundError as e: raise ProjectException(str(e), QLogsColor.Error)


    @staticmethod
    def read_version_info(f: typing.TextIO, version_ids: dict) -> dict[str, AddressMapper]:
        mappers = {'default': AddressMapper('default', 'default')}

        comment_regex = re.compile(r'^\s*#')
        empty_line_regex = re.compile(r'^\s*$')
        section_regex = re.compile(r'^\s*\[([a-zA-Z0-9_.]+)\]$')
        extend_regex = re.compile(r'^\s*extend ([a-zA-Z0-9_.]+)\s*(#.*)?$')
        mapping_regex = re.compile(r'^\s*([a-fA-F0-9]{8})-((?:[a-fA-F0-9]{8})|\*)\s*:\s*([-+])0x([a-fA-F0-9]+)\s*(#.*)?$')
        current_version_name: str = None
        current_version: AddressMapper = None

        for line in f:
            line = line.rstrip('\n')

            if empty_line_regex.match(line):
                continue
            if comment_regex.match(line):
                continue

            match = section_regex.match(line)
            if match:
                # New version
                current_version_name = match.group(1)
                if current_version_name in mappers:
                    raise ValueError(f'Versions file contains duplicate version name <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{current_version_name}</span>')

                current_version = AddressMapper(version_ids.get(current_version_name, 'unk'), current_version_name)
                mappers[current_version_name] = current_version
                continue

            if current_version is not None:
                # Try to associate something with the current version
                match = extend_regex.match(line)
                if match:
                    base_name = match.group(1)
                    if base_name not in mappers:
                        raise ValueError(f'Version {current_version_name} extends unknown version <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{base_name}</span>')
                    if current_version.base is not None:
                        raise ValueError(f'Version {current_version_name} already extends a version')

                    current_version.base = mappers[base_name]
                    continue

                match = mapping_regex.match(line)
                if match:
                    start_address = int(match.group(1), 16)
                    if match.group(2) == '*':
                        end_address = 0xFFFFFFFF
                    else:
                        end_address = int(match.group(2), 16)

                    delta = int(match.group(4), 16)
                    if match.group(3) == '-':
                        delta = -delta

                    current_version.add_mapping(start_address, end_address, delta)
                    continue

            raise ProjectException(f'Unrecognised line in versions file: <span style="background-color: #{QLogsColor.Warning.value.hex[1:]}55">{line}</span>', QLogsColor.Warning)

        return mappers


    def _do_mapfile(self, src: str, dest: str, mapper: AddressMapper) -> None:
        new = []
        with open(f'{self._cwd}/{src}', 'r', encoding = 'utf-8') as f:
            mapfile = [x.rstrip() for x in f]

        for line in mapfile:
            pos = line.find('= 0x80')
            if pos != -1:
                oldoffs = line[pos+2:pos+12]
                newoffs = mapper.remap(int(oldoffs, 16))
                line = line.replace(oldoffs, str(newoffs))

            new.append(line + '\n')

        with open(f'{self._cwd}/{dest}', 'w', encoding = 'utf-8') as f:
            f.writelines(new)


    def _work_on_hook(self, hook: dict, mapper: AddressMapper) -> None:
        error = 'Missing hook type'
        try:
            t = hook['type']

            if t == 'patch':
                error = 'Missing address'
                hook[f'addr_{mapper.name}'] = mapper.remap(hook[f'addr_{self._base_version}'])

            elif t == 'branch_insn' or t == 'add_func_pointer':
                error = 'Missing source address'
                hook[f'src_addr_{mapper.name}'] = mapper.remap(hook[f'src_addr_{self._base_version}'])

                if f'target_func_{self._base_version}' in hook:
                    error = 'Missing target function'
                    hook[f'target_func_{mapper.name}'] = mapper.remap(hook[f'target_func_{self._base_version}'])

            elif t == 'nop_insn':
                error = 'Missing area'
                area = hook[f'area_{self._base_version}']

                if isinstance(area, list):
                    start = mapper.remap(area[0])
                    new_area = [start, start + (area[1] - area[0])]
                else:
                    new_area = mapper.remap(area)

                hook[f'area_{mapper.name}'] = new_area

            else:
                raise KeyError()

        except KeyError:
            ret = (f'Key Error <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{error}</span> in {mapper.name}', QLogsColor.Error, False, tuple())
            self.log_simple.emit(*ret)
            self.log_complete.emit(*ret)


    def _do_module(self, src: str, dest: str, mappers: dict[str, AddressMapper]) -> None:
        try:
            with open(f'{self._cwd}/{src}', 'r', encoding = 'utf-8') as f:
                m = yaml.safe_load(f.read())

        except FileNotFoundError as e:
            raise ProjectException(f'Unable to find "<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{e.filename}</span>" at "{self._cwd}"', QLogsColor.Error)
        
        except yaml.MarkedYAMLError as e:
            error = e.problem_mark.get_snippet().split('\n')[0]
            symbols_str = e.problem_mark.get_snippet().split('\n')[1]
            index_start, index_end = symbols_str.find('^'), symbols_str.rfind('^')
            error_highlight = f'{error[:index_start]}<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{error[index_start:index_end+1]}</span>{error[index_end+1:]}'

            error_msg = f'{e.problem} {e.context}'.replace('<', '&lt;').replace('>', '&gt;')

            raise ProjectException(f'Error parsing module file at line {e.problem_mark.line + 1}, column {e.problem_mark.column + 1}: <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{src}</span>\n{error_msg}\n{error_highlight}', QLogsColor.Error)

        for hook in m.get('hooks', []):
            exclude = hook.get('exclude', [])
            if isinstance(exclude, str): exclude = [exclude]

            exclude_inherit = hook.get('exclude_inherit', [])
            if isinstance(exclude_inherit, str): exclude_inherit = [exclude_inherit]
            for e in exclude_inherit:
                for mp in mappers.values():
                    if mp.is_or_inherits_from(e):
                        if mp.name not in exclude:
                            exclude.append(mp.name)

            if exclude: hook['exclude'] = exclude
            if exclude_inherit: del hook['exclude_inherit']

        for x_id, txt_id in self._version_ids.items():
            mapper = mappers[txt_id]
            if 'hooks' in m:
                for hook in m['hooks']:
                    if x_id in hook.get('exclude', []):
                        continue

                    if hook.get('version_specific', False):
                        continue

                    self._work_on_hook(hook, mapper)

        with open(f'{self._cwd}/{dest}', 'w', encoding = 'utf-8') as f:
            f.write(yaml.dump(m))


    def _do_project(self, f: str, already_done: set, mappers: dict[str, AddressMapper]) -> None:
        try:
            with open(f, 'r', encoding = 'utf-8') as infile:
                proj = yaml.safe_load(infile.read())

        except FileNotFoundError as e:
            raise ProjectException(f'Unable to find "<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{e.filename}</span>" at "{self._cwd}"', QLogsColor.Error)

        except yaml.MarkedYAMLError as e:
            error = e.problem_mark.get_snippet().split('\n')[0]
            symbols_str = e.problem_mark.get_snippet().split('\n')[1]
            index_start, index_end = symbols_str.find('^'), symbols_str.rfind('^')
            error_highlight = f'{error[:index_start]}<span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{error[index_start:index_end+1]}</span>{error[index_end+1:]}'

            error_msg = f'{e.problem} {e.context}'.replace('<', '&lt;').replace('>', '&gt;')

            raise ProjectException(f'Error parsing module file at line {e.problem_mark.line + 1}, column {e.problem_mark.column + 1}: <span style="background-color: #{QLogsColor.Error.value.hex[1:]}55">{f}</span>\n{error_msg}\n{error_highlight}', QLogsColor.Error)

        if 'modules' in proj:
            for m in proj['modules']:
                if m not in already_done:
                    already_done.add(m)
                    self._do_module(m.replace('processed/', ''), m, mappers)


    @staticmethod
    def revert_mappers(mappers_base: dict[str, AddressMapper]) -> dict[str, AddressMapper]:
        new_mappers: dict[str, AddressMapper] = {}

        for version, address_mapper in mappers_base.items():
            base = None
            if address_mapper.base:
                base_key = [k for k, v in mappers_base.items() if v == mappers_base[version].base]
                if base_key:
                    base = new_mappers[base_key[0]]

            new_mappers[version] = AddressMapper(address_mapper.name, version, base)

            for mapping in address_mapper.items():
                new_mappers[version].add_mapping(mapping.start + mapping.delta, mapping.end + mapping.delta, -mapping.delta)

        return new_mappers
#----------------------------------------------------------------------
