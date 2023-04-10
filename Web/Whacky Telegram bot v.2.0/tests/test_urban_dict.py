import pytest
from requests.exceptions import InvalidJSONError

from app.config import SERVICE_ERROR_MSG
from app.services.urban_dict import UrbanDict
from tests.fakes import FakeUrbanClient


@pytest.fixture
def setup_test_apps(monkeypatch):
    with monkeypatch.context():
        client = FakeUrbanClient()
        ud = UrbanDict(client)
        yield client, ud
        client.reset()


class TestUrbanDict:
    def test_get_definitions(self, setup_test_apps):
        client, ud = setup_test_apps
        prompt1 = "some prompt"
        response = ud.get_definitions(prompt1)

        assert isinstance(response, str)
        assert client.called

        client.reset()
        prompt2 = ""
        response = ud.get_definitions(prompt2)

        assert isinstance(response, str)
        assert client.called

    def test_get_urban_definition(self, setup_test_apps):
        client, ud = setup_test_apps
        word_or_phrase = "some phrase"
        response = ud.get_urban_definition(word_or_phrase)

        assert isinstance(response, str)
        assert client.called

    def test_get_urban_definition_error(self, monkeypatch, setup_test_apps):
        def raise_exc(*a, **kw):
            raise InvalidJSONError()

        monkeypatch.setattr(FakeUrbanClient, "get_definition", raise_exc)
        client, ud = setup_test_apps
        word_or_phrase = "some phrase"
        response = ud.get_urban_definition(word_or_phrase)

        assert response == SERVICE_ERROR_MSG
        assert not client.called

    def test_get_random_urban_words(self, setup_test_apps):
        client, ud = setup_test_apps
        response = ud.get_random_urban_words()

        assert isinstance(response, str)
        assert client.called

    def test_get_random_urban_words_error(self, monkeypatch, setup_test_apps):
        def raise_exc(*a, **kw):
            raise InvalidJSONError()

        monkeypatch.setattr(FakeUrbanClient, "get_random_definition", raise_exc)
        client, ud = setup_test_apps
        response = ud.get_random_urban_words()

        assert response == SERVICE_ERROR_MSG
        assert not client.called
