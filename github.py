__author__ = 'james'

from itertools import chain

import requests


class GitHub:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": "token {token}".format(token=self.token)}

    def paginate(self, path, params={}):
        response = requests.get("https://api.github.com{path}".format(path=path), params=params, headers=self.headers)

        while response.links.get('next'):
            yield response.json()
            response = requests.get(response.links['next']['url'], headers=self.headers)

        yield response.json()

    def json(self, path, params={}):
        return chain.from_iterable(self.paginate(path, params={}))

    def org_members(self, org, page=0):
        return self.json("/orgs/{org}/members".format(org=org), {"page": page})

    def org_repos(self, org, page=0):
        return self.json("/orgs/{org}/repos".format(org=org), {"page": page})

    def repo_comments(self, owner, repo, page=0):
        return self.json("/repos/{owner}/{repo}/comments".format(owner=owner, repo=repo), {"page": page})

    def repo_events(self, owner, repo, page=0):
        return self.json("/repos/{owner}/{repo}/events".format(owner=owner, repo=repo), {"page": page})

    def repo_commits(self, owner, repo, page=0):
        return self.json("/repos/{owner}/{repo}/commits".format(owner=owner, repo=repo), {"page": page})

    def repo_keys(self, owner, repo, page=0):
        return self.json("/repos/{owner}/{repo}/keys".format(owner=owner, repo=repo), {"page": page})

    def user_events(self, username, page=0):
        return self.json("/users/{username}/events".format(username=username), {"page": page})


def event_to_csv(event):
    return


if __name__ == "__main__":
    client = GitHub(token="")

    for repo in client.org_repos('ORG'):

        print("{repo_name}".format(repo_name=repo['name']))
        for key in client.repo_keys('ORG', repo['name']):
            print("\t{key_url}".format(key_url=key['url']))
