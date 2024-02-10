import os

import httpx
from pathlib import Path
from dotenv import load_dotenv

from conjure.models.annotation import Annotations, Classification, ObjectDetection


class ConjureClient:
    def __init__(self, api_key: str, lazy: bool = False):
        """
        Parameters
        ----------
        `api_key: str`
            The user's API key.

        `lazy: bool = False`
            Whether to key the API key is valid on class initialisation.
        """
        # cache endpoint and key information
        load_dotenv()
        self._url = os.getenv("API_ENDPOINT")
        self._api_key = api_key

        # check that the API key is valid
        if not lazy:
            self._check_api_key()

    def _check_api_key(self):
        """
        Verifies that the API key is valid.
        """
        # check the endpoint and credentials are valid
        headers = {"api-key": self._api_key}
        response = httpx.get(self._url + "/api-key/verify", headers=headers)

        # if the endpoint or credentials are not valid raise an error
        if not response.json():
            msg = (
                "Could not connect to Conjure AI. Please ensure you are using a valid"
                " API key."
            )
            raise ConnectionError(msg)

    def upload_image(
        self, image_file: Path, annotations: list[Classification | ObjectDetection]
    ):
        """
        Upload an image and its annotations to the Conjure API platform.

        Parameters
        ----------
        `image_file: Path`
            A path to a local file to upload.

        `annotations: list[Classification | ObjectDetection]`
            A collection of annotations associated with the image.
        """
        endpoint = self._url + "/data/upload-image"
        headers = {"api-key": self._api_key}
        data = {"annotations": Annotations(annotations=annotations).model_dump_json()}
        files = {
            "image": (
                image_file.name,
                open(image_file, "rb"),
                f"image/{image_file.suffix.replace('.', '')}",
            )
        }
        httpx.post(endpoint, headers=headers, data=data, files=files)
