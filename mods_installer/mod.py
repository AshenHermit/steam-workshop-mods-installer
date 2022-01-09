from typing import List
import requests
import urllib.parse
from pathlib import Path
from tqdm import tqdm

from mods_installer.json_exportable import JSONExportable

class Mod(JSONExportable):
    def __init__(self, id:int=-1, name:str="mod", description:str="", 
                    logo_url:str="", zip_file_url:str="") -> None:
        super().__init__()
        
        self.id = id
        self.name = name
        self.description = description
        self.logo_url = logo_url
        self.zip_file_url = zip_file_url
        self.game_name = ""
        self.game_id = -1
        self.size = -1

    def download_into(self, directory:Path):
        url = self.zip_file_url
        filename = Path(urllib.parse.urlparse(url).path).name
        filepath = (directory / filename).resolve()

        print(f"downloading \"{filename}\"...")

        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(filepath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")

        return filepath

    def __str__(self) -> str:
        if self.size <= 0:
            size_string = "??"
        else:
            size_string = self.size/1000/1000
            size_string = "{:0.2f}".format(size_string)
        return f"<Mod {self.id} - \"{self.name}\" for game \"{self.game_name}\" - {size_string} Mb>"

