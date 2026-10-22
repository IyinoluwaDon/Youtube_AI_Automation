import json
import os

from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import (
    InstalledAppFlow
)

from googleapiclient.discovery import (
    build
)

from googleapiclient.http import (
    MediaFileUpload
)

from app.core.config import settings
from app.core.logger import logger


class YouTubeService:

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload"
    ]

    TOKEN_FILE = "token.json"

    def authenticate(self):

        creds = None

        if os.path.exists(
            self.TOKEN_FILE
        ):

            try:

                creds = (
                    Credentials
                    .from_authorized_user_file(
                        self.TOKEN_FILE,
                        self.SCOPES
                    )
                )

            except Exception:

                os.remove(
                    self.TOKEN_FILE
                )

                creds = None

        if (
            not creds
            or not creds.valid
        ):

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):

                creds.refresh(
                    Request()
                )

            else:

                with open(
                    settings.YOUTUBE_CLIENT_SECRET_FILE,
                    encoding="utf-8"
                ) as client_secret:
                    client_config = json.load(client_secret)

                if "installed" not in client_config:
                    raise ValueError(
                        "YouTube OAuth requires a Desktop app client. "
                        f"Replace '{settings.YOUTUBE_CLIENT_SECRET_FILE}' "
                        "with a Google OAuth client JSON whose top-level "
                        "key is 'installed', then delete token.json and retry."
                    )

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        settings.YOUTUBE_CLIENT_SECRET_FILE,
                        self.SCOPES
                    )
                )

                creds = (
                    flow.run_local_server(
                        host="localhost",
                        port=8765
                    )
                )

            with open(
                self.TOKEN_FILE,
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )

        youtube = build(
            "youtube",
            "v3",
            credentials=creds
        )

        return youtube

    def upload_video(
        self,
        video_path,
        title,
        description
    ):

        youtube = (
            self.authenticate()
        )

        request = (
            youtube.videos()
            .insert(

                part="snippet,status",

                body={

                    "snippet": {

                        "title": title,

                        "description":
                        description,

                        "categoryId":
                        "22"
                    },

                    "status": {

                        "privacyStatus":
                        "public"
                    }
                },

                media_body=
                MediaFileUpload(
                    video_path,
                    resumable=True
                )
            )
        )

        response = (
            request.execute()
        )

        logger.info(
            f"Video Uploaded: "
            f"{response['id']}"
        )

        return {

            "id":
            response["id"],

            "url":
            f"https://www.youtube.com/watch?v={response['id']}"
        }