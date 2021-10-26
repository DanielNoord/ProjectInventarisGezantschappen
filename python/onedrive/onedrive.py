"""Script to download a folder and files from a publicly shared OneDrive link"""
# pylint: disable=too-few-public-methods

import asyncio
import os
from base64 import b64encode
from typing import Optional

import aiofiles
import aiohttp
from requests import Session

ONEDRIVE_PREFIX = "https://api.onedrive.com/v1.0/shares/u!"
ONEDRIVE_SUFFIX = "/root?expand=children"


class OneDrive:
    """
    Downloads shared file/folder to localhost with persisted structure.

    params:
    `str:url`: url to the shared one drive folder or file
    `str:path`: local filesystem path

    methods:
    `download() -> None`: fire async download of all files found in URL
    """

    def __init__(self, url: Optional[str] = None, path: Optional[str] = None) -> None:
        if not (url and path):
            raise ValueError("URL to shared resource or path to download is missing.")

        self.compiled_url = self._compile_url(url)
        self.path = path
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
        )
        self.to_download: list[dict[str, str]] = []
        self.downloaded = 0

    @staticmethod
    def _compile_url(url: str) -> str:
        url_bytes64 = b64encode(bytes(url, "utf-8"))
        return (
            url_bytes64.decode("utf-8").replace("/", "_").replace("+", "-").rstrip("=")
        )

    @staticmethod
    def _token(url: str) -> str:
        return "u!" + b64encode(url.encode()).decode()

    def _traverse_url(self, url: str, name: str = "") -> None:
        """Traverse the folder tree and store leaf urls with filenames"""

        response = self.session.get(f"{ONEDRIVE_PREFIX}{url}{ONEDRIVE_SUFFIX}").json()
        name = name + os.sep + response["name"]

        # shared file
        if not response["children"]:
            file: dict[str, str] = {}
            file["name"] = name.lstrip(os.sep)
            file["url"] = response["@content.downloadUrl"]
            self.to_download.append(file)
            print(f"Found {file['name']}")

        # shared folder
        for child in response["children"]:
            print(child["name"])
            if "folder" in child:
                self._traverse_url(self._compile_url(child["webUrl"]), name)

            if "file" in child:
                file = {}
                file["name"] = (name + os.sep + child["name"]).lstrip(os.sep)
                file["url"] = child["@content.downloadUrl"]
                self.to_download.append(file)
                print(f"Found {file['name']}")

    async def _download_file(
        self, file: dict[str, str], session: aiohttp.ClientSession
    ) -> None:
        async with session.get(file["url"], timeout=None) as response:
            filename = os.path.join(self.path, file["name"])
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            async with aiofiles.open(filename, "wb") as opened_file:
                async for chunk in response.content.iter_chunked(1024 * 16):
                    if chunk:
                        await opened_file.write(chunk)

        self.downloaded += 1
        progress = int(self.downloaded / len(self.to_download) * 100)
        print(f"Download progress: {progress}%")

    async def _downloader(self) -> None:
        async with aiohttp.ClientSession() as session:
            await asyncio.wait(
                [self._download_file(file, session) for file in self.to_download]
            )

    def download(self) -> None:
        """Download the files from the url provided upon class initialisation"""
        print("Traversing public folder\n")
        self._traverse_url(self.compiled_url)

        print("\nStarting async download\n")
        asyncio.get_event_loop().run_until_complete(self._downloader())
