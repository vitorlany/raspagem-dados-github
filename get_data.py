import requests
from dotenv import load_dotenv
import os
import math

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicione seu token de acesso pessoal aqui
token = os.getenv("GITHUB_TOKEN")

# GraphQL
GITHUB_API_URL = "https://api.github.com/graphql"

# Execitar queries
def run_query(query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code}")

# Função para obter os repositórios mais populares com a query "query"
def get_popular_repos(query, num_repos):
    repos = []
    num_pages = math.ceil(num_repos / 100)
    cursor = None

    for _ in range(num_pages):
        fetch_count = min(num_repos, 100)
        pagination = f', after: "{cursor}"' if cursor else ""
        graphql_query = f"""
        {{
          search(query: "{query}", type: REPOSITORY, first: {fetch_count}{pagination}) {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            edges {{
              node {{
                ... on Repository {{
                  name
                  owner {{
                    login
                  }}
                  createdAt
                  updatedAt
                  primaryLanguage {{
                    name
                  }}
                  pullRequests {{
                    totalCount
                  }}
                  releases {{
                    totalCount
                  }}
                  issues(states: OPEN) {{
                    totalCount
                  }}
                  closedIssues: issues(states: CLOSED) {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        result = run_query(graphql_query)
        page_repos = result["data"]["search"]["edges"]
        if not page_repos:
            break

        repos.extend(page_repos)
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        num_repos -= fetch_count

        if not result["data"]["search"]["pageInfo"]["hasNextPage"]:
            break

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
