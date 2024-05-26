import pytest


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
    assert len(emojis) > 0, f"The emoji list should not be empty. Current emoji count: {len(emojis)}"       
    

@pytest.mark.api
def test_specific_emoji_exists(github_api):
    emojis = github_api.get_emojis('')
    if 'ukraine' in emojis:
        print(emojis['ukraine'])
    else:
        print("There is no emoji for the flag of Ukraine")
        
        
# @pytest.mark.api
# def test_print_all_emojis(github_api):
    # emojis = github_api.get_emojis('')
    # print(emojis)
    # # assert False, "Printed all emojis for verification"