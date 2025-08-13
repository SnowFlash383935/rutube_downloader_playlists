import requests
from .rutube import Rutube
from urllib import parse

class Playlist:
    def __init__(self, url):
        try:
            id = int(parse.urlparse(url).path.strip("/").split("/")[1])
        except (IndexError, ValueError):
            raise ValueError(f"Invalid URL: {url}")

        # грузим мета-информацию
        self.info = requests.get(
            f"https://rutube.ru/api/playlist/custom/{id}/?client=wdp"
        ).json()

        # грузим все видео
        self.all_raw = []
        page = 0
        while True:
            chunk = requests.get(
                f"https://rutube.ru/api/playlist/custom/{id}/videos/?client=wdp&page={page}"
            ).json()
            self.all_raw.extend(chunk["results"])
            if not chunk.get("has_next"):
                break
            page += 1

        # кэш: индекс -> объект Rutube
        self._cache = {}

    def __len__(self):
        return len(self.all_raw)

    def __getitem__(self, idx):
        if idx not in self._cache:
            self._cache[idx] = Rutube(self.all_raw[idx]["video_url"])
        return self._cache[idx]
