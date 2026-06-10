import os
import json
import shutil
from pathlib import Path

from app.core.logger import logger


def create_directory(path: str):

    os.makedirs(path, exist_ok=True)

    logger.info(f"Directory Created: {path}")


def save_json(data, filepath):

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    logger.info(f"JSON Saved: {filepath}")


def load_json(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_file(filepath):

    if os.path.exists(filepath):

        os.remove(filepath)

        logger.info(f"Deleted: {filepath}")


def copy_file(src, dst):

    shutil.copy(src, dst)

    logger.info(f"Copied {src} -> {dst}")


def get_file_size(filepath):

    return round(
        os.path.getsize(filepath) / (1024 * 1024),
        2
    )


def ensure_artifact_folders():

    folders = [
        "artifacts/scripts",
        "artifacts/audio",
        "artifacts/subtitles",
        "artifacts/stock_videos",
        "artifacts/rendered_videos",
        "artifacts/thumbnails"
    ]

    for folder in folders:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )

    logger.info("Artifact folders ready.")