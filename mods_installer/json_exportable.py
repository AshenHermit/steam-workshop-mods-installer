from typing import List
from pathlib import Path
import json
import inspect
import traceback

CONFIG_NAME="mods_installer_config"
class JSONExportable:
    def __init__(self, filepath:Path=None) -> None:
        self.__filepath = filepath or (Path(__file__).parent / CONFIG_NAME).resolve()
        self.__filepath = Path(self.__filepath)
        self.__filepath = self.__filepath.with_suffix(".json")

    @property
    def filepath(self):
        return self.__filepath

    def as_dict(self):
        def is_property(attr):
            return isinstance(getattr(type(self), attr, None), property)
        members = inspect.getmembers(self, predicate=lambda x: not inspect.isroutine(x))
        members = list(filter(lambda m: not m[0].startswith("_") and not is_property(m[0]), members))
        data = {}
        for name, value in members:
            try:
                json.dumps(value)
            except:
                value = str(value)
            data[name] = value
        return data
        
    def load_dict(self, data:dict):
        for key, value in data.items():
            if hasattr(self, key):
                if type(getattr(self, key)) is not type(value):
                    continue
            setattr(self, key, value)
        return self

    def load(self):
        try:
            data = self.__filepath.read_text(encoding="utf-8")
            data = json.loads(data)
            self.load_dict(data)
        except FileNotFoundError: pass
        except: traceback.print_exc()
        return self
    
    def save(self):
        try:
            data = self.as_dict()
            json_text = json.dumps(data, ensure_ascii=False, indent=2)
            self.__filepath.write_text(json_text, encoding="utf-8")
        except:
            print(f"failed to save config to file \"{self.__filepath.name}\"")
            traceback.print_exc()
        return self