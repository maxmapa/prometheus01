import requests


class GitHub:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com"

    def get_user(self, username):
        r = requests.get(f"https://api.github.com/users/{username}")
        body = r.json()

        return body

    def search_repo(self, name):
        r = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": name}
        )
        body = r.json()

        return body
        
    def get_emojis(self, emojis):
        r = requests.get("https://api.github.com/emojis")
        body = r.json()

        return body

    def get_commits(self, owner, repo):
        headers = {"Authorization": f"token {self.token}"}
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        r = requests.get(url, headers=headers)
        
        # Handle potential errors
        if r.status_code != 200:
            r.raise_for_status()
        
        return r.json()

    def get_commit(self, owner, repo, sha):
        headers = {"Authorization": f"token {self.token}"}
        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"
        r = requests.get(url, headers=headers)
        
        # Handle potential errors
        if r.status_code != 200:
            r.raise_for_status()
        
        return r.json()