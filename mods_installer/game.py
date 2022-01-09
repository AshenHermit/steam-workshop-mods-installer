import os
from typing import List
import zipfile
from pathlib import Path
import traceback
import shutil

from mods_installer.json_exportable import JSONExportable
from mods_installer.mod import Mod
from mods_installer.mod_loader import SWModLoader

class GameConfig(JSONExportable):
    def __init__(self, filepath:Path=None) -> None:
        super().__init__(filepath)
        self.game_id = -1
        self.mods_ids = []
        self.mods_registry = {}

class Game:
    def __init__(self, root_directory:Path) -> None:
        self.root_directory = root_directory.resolve()
        self.config = GameConfig(self.root_directory / "mods_installer_config.json")
        self.config.load()
        print(f"config will be located in \"{self.config.filepath}\"")
        self.mod_loader = SWModLoader()

    def register_mod_info(self, mod:Mod):
        key = str(mod.id)
        data = mod.as_dict()
        self.config.mods_registry[key] = data
        return data

    def install_mod(self, mod:Mod):
        print()
        self.register_mod_info(mod)
        self.config.mods_ids.append(mod.id)
        self.config.mods_ids = list(set(self.config.mods_ids))
        self.config.game_id = mod.game_id

        temp_folder = self.root_directory / "_mods_downloader_tmp"
        os.makedirs(str(temp_folder), exist_ok=True)
        try:
            zip_filepath = mod.download_into(temp_folder)
            print("unpacking...")
            with zipfile.ZipFile(str(zip_filepath), 'r') as zip_ref:
                zip_ref.extractall(str(self.root_directory))
            print(f"ssuucceessffuullyy installed {mod}")
        except:
            print("failed to install mod")
            traceback.print_exc()
        shutil.rmtree(temp_folder, ignore_errors=True)
        print()

        self.config.save()

    def install_mod_from_query(self, query):
        print(f"fetching mod \"{query}\"...")
        mod = self.mod_loader.fetch_mod_from_query(query)
        self.install_mod(mod)

    def install_mods_from_queries(self, queries:List[str]):
        for query in queries:
            self.install_mod_from_query(query)

    def update_mods(self):
        if len(self.config.mods_ids) == 0:
            print("nothing to update")
        else:
            for mod_id in self.config.mods_ids:
                self.install_mod_from_query(mod_id)

    def render_log(self):
        log = "\n"
        count = len(self.config.mods_ids)
        if count==0:
            log+="no mods registered\n"
        else:
            log += f"registered {count} mods:\n"
            for key, mod_dict in self.config.mods_registry.items():
                mod = Mod()
                mod.load_dict(mod_dict)
                log += f"    {mod}\n"
        return log

    def print_log(self):
        print(self.render_log())