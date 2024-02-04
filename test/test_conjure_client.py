import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from pytest_httpx import HTTPXMock

from conjure import ConjureClient


class TestConjureClient:
    @pytest.fixture
    def url(self) -> str:
        load_dotenv()
        return os.getenv("API_ENDPOINT")

    def test_init(self, url: str, httpx_mock: HTTPXMock):
        # mock the reponse
        httpx_mock.add_response(url=url + "/check-api-key", json=True)

        # try initialising the client
        api_key = str(uuid4())
        client = ConjureClient(api_key, False)

        # check the client was initialised correctly
        assert isinstance(client, ConjureClient)
