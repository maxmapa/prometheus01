import pytest
import requests


@pytest.mark.api
def test_user_exists(github_api):
    user = github_api.get_user('defunkt')

    assert user['login'] == 'defunkt'


@pytest.mark.api
def test_user_not_exists(github_api):
    r = github_api.get_user('butenkosergii')

    assert r['message'] == 'Not Found'


@pytest.mark.api
def test_repo_can_be_found(github_api):
    r = github_api.search_repo('become-qa-auto')

    assert r['total_count'] == 58
    assert 'become-qa-auto' in r['items'][0]['name']


@pytest.mark.api
def test_repo_cannot_be_found(github_api):
    r = github_api.search_repo('sergiibutenko_repo_non_exist')

    assert r['total_count'] == 0


@pytest.mark.api
def test_repo_with_single_char_be_found(github_api):
    r = github_api.search_repo('s')

    assert r['total_count'] != 0


@pytest.mark.api
def test_emoji_list_not_empty(github_api):
    emojis = github_api.get_emoji('')

    assert len(emojis) > 0, f"The emoji list should not be empty. Current emoji count: {len(emojis)}"


@pytest.mark.api
def test_emoji_exist(github_api):
    emojis = github_api.get_emoji('')

    assert 'ukraine' in emojis


@pytest.mark.api
def test_emoji_not_exist(github_api):
    emojis = github_api.get_emoji('')

    assert 'germany' not in emojis


@pytest.mark.api
def test_country_flag_missing(github_api):
    emojis = github_api.get_emoji('')
    eu = [
        "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
        "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
        "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
        "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania",
        "Slovakia", "Slovenia", "Spain", "Sweden"
    ]

    missing_countries = [
        country for country in eu if country.lower() not in emojis
    ]
    missing = ['France', 'Germany', 'Italy', 'Spain']

    assert missing_countries == missing, f"Missing {len(missing_countries)} countries: {', '.join(missing_countries)}"
