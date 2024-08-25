import requests
from dotenv import load_dotenv
import os
import math

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicione seu token de acesso pessoal aqui
token = os.getenv("GITHUB_TOKEN")

# Função para obter os repositórios mais populares com a query "query"
def get_popular_repos(query, num_repos):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    headers = {"Authorization": f"token {token}"}
    num_pages = math.ceil(num_repos / 100)
    page = 1
    repos = []
    while page <= num_pages:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_repos = response.json()["items"]
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        else:
            raise Exception(f"Failed to fetch repositories: {response.status_code}")
    return repos

# Função para obter o número de pull requests com paginação
def get_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all"
    headers = {"Authorization": f"token {token}"}
    page = 1
    pull_requests = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_pull_requests = response.json()
            if not page_pull_requests:
                break
            pull_requests.extend(page_pull_requests)
            page += 1
        else:
            raise Exception(f"Failed to fetch pull requests: {response.status_code}")
    return len(pull_requests)

# Função para obter o número de releases com paginação
def get_releases(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"token {token}"}
    page = 1
    releases = []
    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_releases = response.json()
            if not page_releases:
                break
            releases.extend(page_releases)
            page += 1
        else:
            raise Exception(f"Failed to fetch releases: {response.status_code}")
    return len(releases)

# Função para obter o número de issues fechadas com paginação
def get_closed_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed"
    headers = {"Authorization": f"token {token}"}
    page = 1
    closed_issues = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_closed_issues = response.json()
            if not page_closed_issues:
                break
            closed_issues.extend(page_closed_issues)
            page += 1
        else:
            raise Exception(f"Failed to fetch closed issues: {response.status_code}")
    return len(closed_issues)
