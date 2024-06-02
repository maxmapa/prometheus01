import pytest
from modules.api.clients.gihub import GitHub


class User:

    def __init__(self) -> None:
        self.name = None
        self.second_name = None

    def create(self):
        self.name = 'Sergii'
        self.second_name = 'Butenko'

    def remove(self):
        self.name = ''
        self.second_name = ''


@pytest.fixture
def user():
    user = User()
    user.create()

    yield user

    user.remove()

@pytest.fixture
def github_api():
    token = "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"
    api = GitHub(token)
    yield api
