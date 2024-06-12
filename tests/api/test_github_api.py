import pytest
import requests


@pytest.mark.api
def test_user_exists(github_api):
    user = github_api.get_user('defunkt')
    assert user['login'] == 'defunkt'
    
@pytest.mark.api
def test_my_user_exists(github_api):
    user = github_api.get_user('maxmapa')
    assert user['login'] == 'maxmapa'

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
    emojis = github_api.get_emojis('')
    print(len(emojis))
    assert len(emojis) > 0, f"The emoji list should not be empty. Current emoji count: {len(emojis)}"       
    

@pytest.mark.api
def test_country_emoji_flag(github_api):
    emojis = github_api.get_emojis('')
    eu = [
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czech_Republic",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Ukraine"
    ]

    missing_countries = [country for country in eu if country.lower() not in emojis]
    missing = ['France', 'Germany', 'Italy', 'Spain']
    
    assert missing_countries == missing, f"Missing {len(missing_countries)} countries: {', '.join(missing_countries)}"


@pytest.mark.api #fails with wrong token in conftest.py
def test_get_commits(github_api):
    owner = "maxmapa"
    repo = "prometheus01"
    commits = github_api.get_commits(owner, repo)
    
    assert isinstance(commits, list)
    assert len(commits) > 0  # Ensure that there is at least one commit
    assert 'sha' in commits[0]
    assert 'commit' in commits[0]

@pytest.mark.api #fails with wrong token in conftest.py
def test_get_specific_commit(github_api):
    owner = "maxmapa"
    repo = "prometheus01"
    commits = github_api.get_commits(owner, repo)
    
    # Assuming there is at least one commit
    assert len(commits) > 0
    
    commit_sha = commits[0]['sha']
    commit = github_api.get_commit(owner, repo, commit_sha)
    
    assert commit['sha'] == commit_sha
    assert 'commit' in commit
    assert 'author' in commit