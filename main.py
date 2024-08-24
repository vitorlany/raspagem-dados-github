import requests
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicione seu token de acesso pessoal aqui
token = os.getenv("GITHUB_TOKEN")

# Função para obter os repositórios mais populares com a query "query"
def get_popular_repos(query, num_repos):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={num_repos}"
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

# Função para calcular idade a partir da data "created_at"
def calculate_age(created_at):
    created_at_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    current_at_date = datetime.now()
    age = current_at_date.year - created_at_date.year
    return age

# Função para calcular dias a partir da data "date"
def calculate_days(date):
    created_at_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date()
    current_at_date = datetime.now().date()
    delta = current_at_date - created_at_date
    return delta.days

# Função para coletar e imprimir informações dos repositórios
def collect_and_print_repo_info(repos):
    header = ["repo_name", "created_at", "age", "pull_requests", "releases", "updated_at", "language", "open_issues", "closed_issues", "closed_issues_percent"]
    rows = []

    for repo in repos:
        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        created_at = repo["created_at"]
        age = calculate_age(created_at)
        pull_requests = get_pull_requests(owner, repo_name) # Procurar otimizar, consome muito
        releases = get_releases(owner, repo_name)
        updated_at = repo["updated_at"]
        language = repo["language"]
        open_issues = repo["open_issues"]
        closed_issues = get_closed_issues(owner, repo_name) # Procurar otimizar, consome muito

        closed_issues_percent = 0
        if open_issues > 0:
            closed_issues_percent = closed_issues/open_issues

        rows.append([repo_name, created_at, age, pull_requests, releases, updated_at, language, open_issues, closed_issues, closed_issues_percent])
        
    with open('repo_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

# Main
if __name__ == "__main__":
    query = "stars:>0"
    num_repos = 2 # Número de repositórios a serem coletados
    try:
        popular_repos = get_popular_repos(query, num_repos)
        collect_and_print_repo_info(popular_repos)
    except Exception as e:
        print(e)
    exit(0)
