import requests

from pathlib import Path

from app.core.config import settings
from app.core.logger import logger


class StockVideoService:

    def __init__(self):

        self.api_key = settings.PIXABAY_API_KEY

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

    def fetch_pixabay_video(self, keyword, orientation):
        try:
            response = requests.get(
                "https://pixabay.com/api/videos/",
                params={
                    "key": self.api_key,
                    "q": keyword,
                    "per_page": 3,
                    "orientation": orientation
                },
                timeout=20
            )
            response.raise_for_status()
            videos = response.json().get("hits", [])

            if not videos:
                logger.warning(f"Pixabay: no results for keyword '{keyword}'")
                return None

            video_variants = videos[0].get("videos", {})
            for size in ("medium", "small", "tiny"):
                video = video_variants.get(size)
                if video and video.get("url"):
                    return video["url"]

            logger.warning(
                f"Pixabay: no usable video URL for keyword '{keyword}'"
            )
            return None

        except Exception as e:
            logger.error(f"Pixabay Error for '{keyword}': {e}")
            return None

    def download_clips(self, keywords: list, orientation: str):
        clips = []
        output_dir = Path("artifacts/stock_videos")
        output_dir.mkdir(parents=True, exist_ok=True)

        for idx, keyword in enumerate(keywords, start=1):
            url = self.fetch_pixabay_video(keyword, orientation)

            # Fallback: try simpler/broader keyword
            if not url:
                fallback = keyword.split()[0]  # first word only
                logger.warning(f"Retrying with fallback keyword: '{fallback}'")
                url = self.fetch_pixabay_video(fallback, orientation)

            if not url:
                logger.warning(f"Skipping keyword '{keyword}' — no video found")
                continue

            filepath = output_dir / f"clip_{idx}.mp4"
            self._download_file(url, filepath)
            clips.append(filepath)

        return clips