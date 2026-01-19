import os
import requests
import json
from datetime import datetime, timedelta

def run_query(query, variables=None):
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise Exception("GH_TOKEN environment variable not set.")
    
    headers = {"Authorization": f"Bearer {token}"}
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

def get_github_stats():
    # GraphQL Query - Fetch repos for total count and stars
    query = """
    query {
      viewer {
        login
        repositories(first: 100, ownerAffiliations: [OWNER], isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
          totalCount
          nodes {
            name
            stargazerCount
            languages(first: 10) {
              edges {
                size
                node {
                  name
                }
              }
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    
    try:
        result = run_query(query)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    data = result["data"]["viewer"]
    
    # 1. Total Repositories
    total_repos = data["repositories"]["totalCount"]
    
    # 2. Total Stars
    repos = data["repositories"]["nodes"]
    total_stars = sum(repo["stargazerCount"] for repo in repos)
    
    # 3. Calculate Total LOC (from language sizes)
    language_sizes = {}
    for repo in repos:
        if not repo["languages"]["edges"]:
            continue
        for edge in repo["languages"]["edges"]:
            lang_name = edge["node"]["name"]
            size = edge["size"]
            language_sizes[lang_name] = language_sizes.get(lang_name, 0) + size
    
    total_bytes = sum(language_sizes.values())
    total_loc = int(total_bytes / 40)

    # 4. Current Year Contributions (contributionsCollection is last 12 months by default)
    current_year_contributions = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    
    # 5. Active Projects (Last 90 Days)
    # Count repos with activity in last 90 days
    ninety_days_ago = (datetime.now() - timedelta(days=90)).isoformat()
    active_projects = 0
    
    # Need to fetch pushed_at for each repo - we'll use a separate query for this
    # For now, let's use a simple REST API call for each repo to get pushed_at
    for repo in repos[:20]:  # Limit to top 20 to avoid rate limits
        repo_name = repo["name"]
        try:
            rest_url = f"https://api.github.com/repos/{data['login']}/{repo_name}"
            headers = {"Authorization": f"Bearer {os.environ.get('GH_TOKEN')}"}
            resp = requests.get(rest_url, headers=headers)
            if resp.status_code == 200:
                repo_data = resp.json()
                pushed_at = repo_data.get("pushed_at", "")
                if pushed_at >= ninety_days_ago:
                    active_projects += 1
        except:
            pass
    
    stats = {
        "total_repos": total_repos,
        "active_projects": active_projects,
        "current_year_contributions": current_year_contributions,
        "total_loc": total_loc,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    with open("data/github_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    print("Impact Dashboard Updated:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    get_github_stats()
