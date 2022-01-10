import os
from typing import Generator, List
import zipfile
from pathlib import Path
import traceback
import shutil


from requests.api import request
from tqdm import tqdm

from mods_installer.json_exportable import JSONExportable
from mods_installer.mod import Mod
from mods_installer.mod_loader import ModLoader, SWModLoader
from mods_installer.utils import print_error, print_minor, print_success

#TODO: name ModsLibrary is more relevant
class GameConfig(JSONExportable):
    def __init__(self, filepath:Path=None) -> None:
        super().__init__(filepath)
        self.game_id = -1
        self.mods_registry = {}

    @property
    def mods_count(self):
        return len(self.mods_registry.keys())

    @property
    def ids(self):
        return list(map(lambda x: int(x), self.mods_registry.keys()))

    @property
    def mods(self) -> List[Mod]:
        mods = []
        for id in self.ids:
            mod = self.get_mod_by_id(id)
            mods.append(mod)
        return mods

    def get_mod_by_id(self, mod_id:int) -> Mod:
        mod = Mod()
        if mod_id == -1: return None
        key = str(mod_id)
        if key not in self.mods_registry: return None
        mod.load_dict(self.mods_registry[key])
        return mod

    def get_mod_from_query(self, query) -> Mod:
        mod_id = ModLoader.get_mod_id_from_query(query)
        return self.get_mod_by_id(mod_id)

    def register_mod(self, mod:Mod):
        key = str(mod.id)
        data = mod.as_dict()
        self.mods_registry[key] = data
        return data

    def unregister_mod(self, mod:Mod):
        key = str(mod.id)
        self.mods_registry.pop(key)

class Game:
    def __init__(self, root_directory:Path) -> None:
        self.root_directory = root_directory.resolve()
        self.config = GameConfig(self.root_directory / "mods_installer_config.json")
        self.config.load()
        print_minor(f"config will be located in \"{self.config.filepath}\"")
        self.mod_loader = SWModLoader()

    def install_mod(self, mod:Mod):
        self.config.game_id = mod.game_id

        temp_folder = self.root_directory / "_mods_downloader_tmp"
        os.makedirs(str(temp_folder), exist_ok=True)
        try:
            zip_filepath = mod.download_into(temp_folder)
            print_minor("unpacking...")
            with zipfile.ZipFile(str(zip_filepath), 'r') as zip_ref:
                namelist = zip_ref.namelist()
                mod.related_files = list(filter(lambda x: not x.endswith("/"), namelist))
                mod.related_dirs = list(filter(lambda x: x.endswith("/"), namelist))
                zip_ref.extractall(str(self.root_directory))
            self.config.register_mod(mod)
            print_success(f"ssuucceessffuullyy installed {mod}")
        except:
            print_error("failed to install mod")
            traceback.print_exc()
        shutil.rmtree(temp_folder, ignore_errors=True)
        print()

        self.config.save()

    def install_mod_from_query(self, query):
        print(f"fetching mod \"{query}\"...")
        mod = self.mod_loader.fetch_mod_from_query(query)
        self.install_mod(mod)

    def remove_mod(self, mod:Mod, remove_empty_folders=True):
        print(f"removing {mod}...")
        
        pbar = tqdm(total=len(mod.related_files))
        for rel_filepath in mod.related_files:
            filepath = (self.root_directory / Path(rel_filepath)).resolve()
            pbar.set_postfix_str(filepath.name)
            try:
                os.remove(str(filepath))
            except: pass
            pbar.update(1)
        pbar.close()
        
        if remove_empty_folders:
            dirs = reversed(sorted(
                mod.related_dirs, 
                key=lambda x: len(Path(x).parts)))
            for rel_dir in dirs:
                rel_dir = Path(rel_dir)
                abs_dir = (self.root_directory / rel_dir).resolve()
                if abs_dir.exists():
                    if len(os.listdir(abs_dir))==0:
                        shutil.rmtree(abs_dir)
        
        self.config.unregister_mod(mod)
        self.config.save()
        print_success(f"removed.")
        print()

    def remove_mod_from_query(self, query, remove_empty_folders=True):
        mod = self.config.get_mod_from_query(query)
        if mod is None:
            print_error(f"mod \"{query}\" not found")
            return
        self.remove_mod(mod, remove_empty_folders)

    def remove_all_mods(self, remove_empty_folders=True):
        for mod in self.config.mods:
            self.remove_mod(mod, remove_empty_folders)

    def check_mods_for_defects(self):
        for mod in self.config.mods:
            defects_count = 0
            defects = []
            for rfile in mod.related_files:
                rfile = Path(rfile)
                filepath = Path(self.root_directory / rfile).resolve()
                if not filepath.exists():
                    defects_count += 1
                    defects.append(rfile.as_posix())
            
            if len(defects)>0:
                print_error(f"\n    {len(defects)} files missing in mod {mod}:")
                for defect in defects:
                    print_error(f"        {defect}")
                print()

    def update_mods(self):
        if self.config.mods_count == 0:
            print("nothing to update")
        else:
            ids = self.config.ids
            for mod_id in ids:
                self.install_mod_from_query(mod_id)

    def render_log(self):
        log = "\n"
        count = self.config.mods_count
        if count==0:
            log+="no mods registered\n"
        else:
            log += f"registered {count} mods:\n"
            for key in self.config.mods_registry.keys():
                mod = self.config.get_mod_from_query(key)
                log += f"    {mod}\n"
        return log

    def print_log(self):
        print(self.render_log())