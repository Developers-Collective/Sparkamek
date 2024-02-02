#----------------------------------------------------------------------

    # Libraries
from PySide6.QtCore import Signal, QThread
import os, yaml, traceback

from data.lib.qtUtils import QBaseApplication
from ..compiler import *
#----------------------------------------------------------------------

    # Class
class SpritesAndActorsWorker(QThread):
    done = Signal()
    error = Signal(str)

    found_item = Signal(str, int, int, bool)

    @staticmethod
    def init(app: QBaseApplication) -> None:
        pass

    def __init__(self, path: str) -> None:
        super(SpritesAndActorsWorker, self).__init__()

        self._path = path
        self._cwd = os.path.dirname(self._path)

    def run(self) -> None:
        try:
            profiles = {}
            sprites = {'-1': -1}
            if os.path.isfile(f'{self._cwd}/src/profileid.h') or os.path.isfile(f'{self._cwd}/include/profileid.h'):
                if os.path.isfile(f'{self._cwd}/src/profileid.h'): profileid_path = f'{self._cwd}/src/profileid.h'
                else: profileid_path = f'{self._cwd}/include/profileid.h'

                with open(profileid_path, 'r') as f:
                    profileid_data = f.read()

                def find_enum_start(content: str, *searches: str) -> int:
                    total_index = 0

                    for search in searches:
                        index = content.find(search)
                        if index == -1: return -1

                        total_index += index + len(search)
                        content = content[index + len(search):]

                    return total_index

                def find_enum_end(content: str, find: str, rfind: str) -> int:
                    index = content.find(find)
                    if index == -1: return -1

                    content = content[:index]

                    index = content.rfind(rfind)
                    if index == -1: return -1

                    return index

                sprite_id_start = find_enum_start(profileid_data, 'namespace SpriteId', 'enum', '{')
                sprite_id_end = sprite_id_start + find_enum_end(profileid_data[sprite_id_start:], '};', 'Num')
                sprite_id_data = (d.split(',')[0].replace('\t', '').replace('\r', '').replace(' ', '') for d in profileid_data[sprite_id_start:sprite_id_end].split('\n'))

                last_sprite_id = 0
                skip_until_end_of_comment = False

                for sprite_id in sprite_id_data:
                    if sprite_id.startswith('#') or sprite_id.startswith('//') or sprite_id == 'Num' or sprite_id == '': continue
                    if sprite_id.startswith('/*'): skip_until_end_of_comment = True
                    if skip_until_end_of_comment:
                        if sprite_id.endswith('*/'): skip_until_end_of_comment = False
                        continue

                    info = sprite_id.split(',')[0].split('=')

                    if len(info) == 2:
                        name, id = info
                        last_sprite_id = int(id)

                    else:
                        name = info[0]
                        last_sprite_id += 1
                        id = last_sprite_id

                    sprites[name] = int(id)

                profile_id_start = find_enum_start(profileid_data, 'namespace ProfileId', 'enum', '{')
                profile_id_end = profile_id_start + find_enum_end(profileid_data[profile_id_start:], '};', 'Num')
                profile_id_data = (d.split(',')[0].replace('\t', '').replace('\r', '').replace(' ', '') for d in profileid_data[profile_id_start:profile_id_end].split('\n'))

                last_profile_id = 0
                skip_until_end_of_comment = False

                for profile_id in profile_id_data:
                    if profile_id.startswith('#') or profile_id.startswith('//') or profile_id == 'Num' or profile_id == '': continue
                    if profile_id.startswith('/*'): skip_until_end_of_comment = True
                    if skip_until_end_of_comment:
                        if profile_id.endswith('*/'): skip_until_end_of_comment = False
                        continue

                    info = profile_id.split(',')[0].split('=')

                    if len(info) == 2:
                        name, id = info
                        last_profile_id = int(id)

                    else:
                        name = info[0]
                        last_profile_id += 1
                        id = last_profile_id

                    profiles[name] = int(id)

            with open(self._path, 'r') as f:
                data = yaml.safe_load(f)

            for module in data.get('modules', []):
                module_path = f'{self._cwd}/{os.path.basename(module)}'

                if not os.path.isfile(module_path): continue

                with open(module_path, 'r') as f:
                    module_data = yaml.safe_load(f)
                    f.seek(0)
                    module_raw_data = f.read()

                commented_lines = [line for line in module_raw_data.split('\n') if line.startswith('#')]
                replaced_actors = [line for line in commented_lines if 'Replaces Actor ' in line]

                for actor in replaced_actors:
                    try:
                        actor = actor[1:].replace('Replaces Actor ', '').strip()
                        if (sprite_char_id := actor.find('(Sprite ')) == -1: continue
                        sprite = actor[sprite_char_id + 8:].split(')')[0]

                        actor_info = actor[:sprite_char_id].strip().split(' ')
                        actor = actor_info[0]
                        actor_name = actor_info[1] if len(actor_info) > 1 else None

                        self.found_item.emit(actor_name, int(actor), int(sprite), True)

                    except Exception: continue

                if replaced_actors: continue

                for source_file in module_data.get('source_files', []):
                    if not source_file.lower().endswith('.cpp'): continue

                    source_file_path = f'{self._cwd}/{source_file.replace("../", "")}'
                    if not os.path.isfile(source_file_path): continue

                    with open(source_file_path, 'r') as f:
                        source_file_data = f.read()

                    profile_lines = [line for line in source_file_data.split('\n') if line.startswith('Profile ') and 'ProfileId::' in line] #and 'SpriteId::' in line]
                    for profile in profile_lines:
                        try:
                            args = profile.replace(' ', '').strip().split('(')[1].split(')')[0].split(',')
                            if args[1] == '0': sprite_name = '-1'
                            else: sprite_name = args[1].split('::')[1]
                            profile_name = args[4].split('::')[1]

                            if (sprite_id := sprites.get(sprite_name, None)) is None: continue
                            if (profile_id := profiles.get(profile_name, None)) is None: continue

                            self.found_item.emit(profile_name, profile_id, sprite_id, profile_id <= 703)

                        except Exception: continue


        except Exception as e:
            traceback.print_exc()
            self.error.emit(str(e))
            return
        
        self.done.emit()
#----------------------------------------------------------------------
