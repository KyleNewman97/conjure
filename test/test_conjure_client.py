import os
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import pytest
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from pytest_httpx import HTTPXMock

from conjure import ConjureClient
from conjure.models.annotation import BoundingBox, Classification, ObjectDetection


class TestConjureClient:
    @pytest.fixture
    def url(self) -> str:
        load_dotenv()
        return os.getenv("API_ENDPOINT")

    def test_init(self, url: str, httpx_mock: HTTPXMock):
        """
        Test that the client can be initialised and the API key can be verified.
        """
        # mock the reponse
        httpx_mock.add_response(url=url + "/api-key/verify", json=True)

        # try initialising the client
        api_key = str(uuid4())
        client = ConjureClient(api_key, False)

        # check the client was initialised correctly
        assert isinstance(client, ConjureClient)

    def test_upload_image(self, url: str, httpx_mock: HTTPXMock):
        """
        Test that an image and annotations can be uploaded.
        """
        # mock
        httpx_mock.add_response(url=url + "/data/upload-image")

        api_key = str(uuid4())
        client = ConjureClient(api_key, True)

        # define annotations
        annotations = [
            Classification(class_name="person"),
            ObjectDetection(
                class_name="person",
                bounding_box=BoundingBox(center_x=0, center_y=10, width=20, height=30),
            ),
        ]

        # try to upload an image
        with TemporaryDirectory() as temp_dir:
            # create a random image
            temp_file = Path(temp_dir) / "test.png"
            img = np.random.randint(0, 255, (128, 64, 3), dtype=np.uint8)
            Image.fromarray(img).save(temp_file)

            client.upload_image(temp_file, annotations)
