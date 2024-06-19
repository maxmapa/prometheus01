from modules.ui.page_objects.sign_in_page import SignInPage
import pytest


@pytest.mark.ui
def test_incorrect_username_login():
    sign_in_page = SignInPage()

    sign_in_page.go_to()

    sign_in_page.try_login("page_object@gmail.com", "wrong-password")

    assert sign_in_page.check_title("Sign in to GitHub · GitHub")
    
    sign_in_page.close()


@pytest.mark.ui
def test_goto_signup_page():
    sign_in_page = SignInPage()

    sign_in_page.go_to()

    sign_in_page.try_login("page_object@gmail.com", "wrong-password")

    assert sign_in_page.check_title("Sign in to GitHub · GitHub")
    
    sign_in_page.driver.get("https://github.com/signup?source=login")
    
    assert sign_in_page.check_title("Join GitHub · GitHub")
    
    sign_in_page.close()