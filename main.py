import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicione seu token de acesso pessoal aqui
token = os.getenv("GITHUB_TOKEN")

# Função para obter os repositórios mais populares com a palavra-chave "microservices"
def get_popular_repos(keyword, num_repos):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page={num_repos}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code}")

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

# Função para coletar e imprimir informações dos repositórios
def collect_and_print_repo_info(repos):
    for repo in repos:
        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        created_at = repo["created_at"]
        pull_requests = get_pull_requests(owner, repo_name)
        releases = get_releases(owner, repo_name)
        updated_at = repo["updated_at"]
        language = repo["language"]
        open_issues = repo["open_issues"]
        closed_issues = get_closed_issues(owner, repo_name)

        print(f"Repository: {repo_name}")
        print(f'Create at: {created_at}')
        print(f'Pull requests: {pull_requests}')
        print(f'Releases: {releases}')
        print(f'Updated at: {updated_at}')
        print(f'Language: {language}')
        print(f'Open issues: {open_issues}')
        print(f'Closed issues: {closed_issues}')
        print("-" * 200)

# Main
if __name__ == "__main__":
    keyword = "java"
    num_repos = 1 # Número de repositórios a serem coletados
    try:
        popular_repos = get_popular_repos(keyword, num_repos)
        collect_and_print_repo_info(popular_repos);
    except Exception as e:
        print(e)
    exit(0);
