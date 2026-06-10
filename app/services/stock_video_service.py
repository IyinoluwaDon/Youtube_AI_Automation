import requests

from pathlib import Path

from app.core.config import settings
from app.core.logger import logger


class StockVideoService:

    def __init__(self):

        self.api_key = settings.PEXELS_API_KEY

    def _download_file(
        self,
        url,
        filepath
    ):

        response = requests.get(
            url,
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        with open(filepath, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):
                file.write(chunk)

        return filepath

    def fetch_pexels_video(self, keyword):
        try:
            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": self.api_key},
                params={"query": keyword, "per_page": 1, "orientation": "portrait"},
                timeout=20
            )
            response.raise_for_status()
            videos = response.json().get("videos", [])

            if not videos:
                logger.warning(f"Pexels: no results for keyword '{keyword}'")  # ← add this
                return None

            files = sorted(videos[0]["video_files"], key=lambda x: x.get("height", 0), reverse=True)
            return files[0]["link"]

        except Exception as e:
            logger.error(f"Pexels Error for '{keyword}': {e}")  # ← include keyword
            return None

    def download_clips(self, keywords: list):
        clips = []
        output_dir = Path("artifacts/stock_videos")
        output_dir.mkdir(parents=True, exist_ok=True)

        for idx, keyword in enumerate(keywords, start=1):
            url = self.fetch_pexels_video(keyword)

            # Fallback: try simpler/broader keyword
            if not url:
                fallback = keyword.split()[0]  # first word only
                logger.warning(f"Retrying with fallback keyword: '{fallback}'")
                url = self.fetch_pexels_video(fallback)

            if not url:
                logger.warning(f"Skipping keyword '{keyword}' — no video found")
                continue

            filepath = output_dir / f"clip_{idx}.mp4"
            self._download_file(url, filepath)
            clips.append(filepath)

        return clips