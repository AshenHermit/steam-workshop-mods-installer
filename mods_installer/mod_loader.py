from os import stat
from typing import List
import requests
import urllib.parse
from pathlib import Path
import json
import traceback
import time

from mods_installer.mod import Mod

class SteamWorkshopDownloaderIOApI():
    """ https://steamworkshopdownloader.io/
    """
    def __init__(self) -> None:
        self.request_url = "https://node03.steamworkshopdownloader.io/prod/api/download/request"
        # yep, this is odd, but the info is at /file/, and the file is at /status/
        self.file_url = "https://node03.steamworkshopdownloader.io/prod/api/download/status"
        self.info_url = " https://node03.steamworkshopdownloader.io/prod/api/details/file"
        self.session = requests.Session()

    def fetch_mod_info(self, mod_id:int)->dict:
        payload = [mod_id]
        try:
            res = self.session.post(self.info_url, json=payload)
            data = res.json()
            info = data[0]
            return info
        except:
            traceback.print_exc()
            return None

    def fetch_mod_uuid(self, mod_id:int):
        payload = {"publishedFileId": mod_id,"collectionId":None,"hidden":False,"downloadFormat":"raw","autodownload":False}
        try:
            res = self.session.post(self.request_url, json=payload)
            data = res.json()
            uuid = data.get("uuid", None)
            return uuid
        except:
            traceback.print_exc()
            return None
        
    def fetch_file_url_by_uuid(self, uuid:str):
        payload = {"uuids": [uuid]}
        try:
            progress = 0
            while progress<100:
                res = self.session.post(self.file_url, json=payload)
                data = res.json()
                if uuid not in data: return None
                info = data.get(uuid, {})

                progress = info.get("progress", 0)
                if progress!=100: time.sleep(0.5)
                
            if "storageNode" not in info or "storagePath" not in info: 
                return None
            storage_node = info.get("storageNode", "")
            storage_path = info.get("storagePath", "")
            url = f"http://{storage_node}/prod/storage/{storage_path}?uuid={uuid}"
            return url

        except:
            traceback.print_exc()
            return None

    def fetch_mod_file_url_by_id(self, mod_id:int):
        uuid = self.fetch_mod_uuid(mod_id)
        if uuid is None: return None
        file_url = self.fetch_file_url_by_uuid(uuid)
        return file_url

class ModLoader:
    """
    note: not just common mod loader, but steam mod loader, because of reading id from url
    """
    def __init__(self) -> None:
        pass

    def fetch_mod_with_id(self, id:int) -> Mod:
        return Mod(id)

    @staticmethod
    def get_mod_id_from_url(url:str):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        id = query.get("id", None)
        if id is None: return None
        id = id[0]
        id = json.loads(id)
        return id

    @staticmethod
    def get_mod_id_from_query(query):
        id = -1
        query = str(query)
        try:
            if query.startswith("http"):
                id = ModLoader.get_mod_id_from_url(query)
            else:
                id = int(query)
        except: pass
        return id

    def fetch_mod_from_url(self, url:str) -> Mod:
        id = self.get_mod_id_from_url(url)
        return self.fetch_mod_with_id(id)

    def fetch_mod_from_query(self, query):
        mod_id = self.get_mod_id_from_query(query)
        if mod_id == -1: return None
        mod = self.fetch_mod_with_id(mod_id)
        if mod is None: print(f"failed to fetch mod identified as {query}")
        return mod

class SWModLoader(ModLoader):
    def __init__(self) -> None:
        super().__init__()
        self.api = SteamWorkshopDownloaderIOApI()

    def fetch_mod_with_id(self, mod_id: int) -> Mod:
        mod = Mod(mod_id)
        mod.zip_file_url = self.api.fetch_mod_file_url_by_id(mod_id)
        info = self.api.fetch_mod_info(mod_id)
        if info is not None:
            mod.size = int(info.get("file_size", -1))
            mod.name = info.get("title", "")
            mod.description = info.get("file_description", "")
            mod.game_name = info.get("app_name", "")
            mod.logo_url = info.get("preview_url", "")
            mod.game_id = info.get("consumer_appid", -1)
        return mod