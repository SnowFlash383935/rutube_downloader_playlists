import requests
from .rutube import Rutube
from urllib import parse

class Playlist:
    def __init__(self, url):
        try:
            id = int(parse.urlparse(url).path[1:-1].split("/")[1])
        except:
            raise ValueError(f"Invalid URL: {url}!")
        page = 0
        self.info = requests.get(f"https://rutube.ru/api/playlist/custom/{id}/?client=wdp").json()
        result = requests.get(f"https://rutube.ru/api/playlist/custom/{id}/videos/?client=wdp&page={page}").json()
        self.all_raw = result["results"]
        while result["has_next"]:
            page += 1
            result = requests.get(f"https://rutube.ru/api/playlist/custom/{id}/videos/?client=wdp&page={page}").json()
            self.all_raw += result["results"]
    def __len__(self):
        return len(self.all_raw)
    def __getitem__(self, itemnum):
        return Rutube(self.all_raw[itemnum]["video_url"])

