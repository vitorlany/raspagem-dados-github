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

# Executar query do GraphQL
def run_query(query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code} {response.json()}")
    
# Construir query do GraphQL para 'num_repos' repositórios a partir do item 'cursor'
def get_query(query, num_repos, cursor):
    return f"""
        {{
          search(query: "{query}", type: REPOSITORY, first: {num_repos}, after: "{cursor}") {{
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

# Função para obter os repositórios mais populares com a query "query"
def get_popular_repos(query, num_repos):
    repos = []
    max_per_page = 25
    num_pages = math.ceil(num_repos / max_per_page)
    page = 1
    cursor = ""

    while page <= num_pages:
        graphql_query = get_query(query, max_per_page, cursor)

        result = run_query(graphql_query)
        page_repos = result["data"]["search"]["edges"]
        if not page_repos:
            break

        repos.extend(page_repos)
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        page += 1

    return repos
