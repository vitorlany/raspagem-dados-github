from get_data import *
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicione seu token de acesso pessoal aqui
token = os.getenv("GITHUB_TOKEN")

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
    num_repos = 1000 # Número de repositórios a serem coletados
    try:
        popular_repos = get_popular_repos(query, num_repos)
        collect_and_print_repo_info(popular_repos)
    except Exception as e:
        print(e)
    exit(0)
