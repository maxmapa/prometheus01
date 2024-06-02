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
    assert r['total_count'] == 57
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
def test_specific_emoji_exists(github_api):
    emojis = github_api.get_emojis('')
    eu = [
    "austria",
    "belgium",
    "bulgaria",
    "croatia",
    "cyprus",
    "czech republic",
    "denmark",
    "estonia",
    "finland",
    "france",
    "germany",
    "greece",
    "hungary",
    "ireland",
    "italy",
    "latvia",
    "lithuania",
    "luxembourg",
    "malta",
    "netherlands",
    "poland",
    "portugal",
    "romania",
    "slovakia",
    "slovenia",
    "spain",
    "sweden",
    "ukraine"
]
    missing_countries = [country for country in eu if country not in emojis]

    if missing_countries:
        for country in missing_countries:
            print(country, "is not in emojis")
        return None
    else:
        assert r.status_code == 200
print(test_specific_emoji_exists())

    # if 'ukraine' in emojis:
        # print("URL is ", emojis['ukraine'])
    # else:
        # print("There is no emoji for the flag of Ukraine")
        
# @pytest.mark.api
# def test_second_emoji_request(github_api):
    # emojis = github_api.get_emojis('')
    # body = r.json()
    # headers = r.headers

    # assert body['germany'] == True
    # assert r.status_code == 200 if 'germany' in emojis       
        
        
# @pytest.mark.api
# def test_print_all_emojis(github_api):
    # emojis = github_api.get_emojis('')
    # print(emojis)
    # # assert False, "Printed all emojis for verification"