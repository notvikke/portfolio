import os
import requests
import json
from datetime import datetime

def get_github_stats():
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("Error: GH_TOKEN environment variable not set.")
        return

    headers = {"Authorization": f"token {token}"}
    username = ""
    
    # First get the authenticated user's login
    try:
        user_resp = requests.get("https://api.github.com/user", headers=headers)
        user_resp.raise_for_status()
        username = user_resp.json()["login"]
    except Exception as e:
        print(f"Error fetching user: {e}")
        return

    repos_url = f"https://api.github.com/user/repos?type=owner&per_page=100"
    repos = []
    page = 1

    try:
        while True:
            resp = requests.get(f"{repos_url}&page={page}", headers=headers)
            resp.raise_for_status()
            page_repos = resp.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return

    total_size_kb = 0
    total_loc = 0
    
    # Standard estimate: 1 LOC approx 40 bytes? 
    # Actually, the user asked to: "sum all language bytes and divide by 40"
    # So we need to fetch /languages for each repo.
    
    # To avoid API rate limits (5000/hr), fetching /languages for ALL repos might be heavy if user has many repos.
    # But for a portfolio, typically < 100 repos.
    
    print(f"Analyzing {len(repos)} repositories...")

    query_count = 0
    
    for repo in repos:
        if repo["fork"]:
            continue
            
        total_size_kb += repo["size"]
        
        # Get languages
        languages_url = repo["languages_url"]
        try:
            lang_resp = requests.get(languages_url, headers=headers)
            if lang_resp.status_code == 200:
                languages = lang_resp.json()
                repo_bytes = sum(languages.values())
                total_loc += repo_bytes / 40
            query_count += 1
            if query_count % 10 == 0:
                print(f"Processed {query_count} repos language stats...")
        except Exception as e:
            print(f"Error fetching languages for {repo['name']}: {e}")

    stats = {
        "total_size_mb": round(total_size_kb / 1024, 2),
        "total_loc": int(total_loc),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    with open("data/github_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    print("Stats updated successfully:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    get_github_stats()
