import os
import re
import requests
import datetime

# Configuration
GH_TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {GH_TOKEN}"} if GH_TOKEN else {}

PROJECT_FILES = [
    r"content/project/storyline-io/index.md",
    r"content/project/legalese-ai/index.md",
    r"content/project/aether-glide/index.md",
    r"content/project/nse-trade-simulation/index.md",
    r"content/project/automated-certificate-tracker/index.md",
    r"content/project/budgetroam/index.md"
]

def get_repo_date(repo_url):
    """Fetches the last pushed_at date for a GitHub repository."""
    # Extract owner/repo from URL (e.g., https://github.com/notvikke/Legalese.ai)
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        print(f"Skipping non-GitHub URL: {repo_url}")
        return None
    
    owner, repo = match.groups()
    repo = repo.strip().rstrip("/") # Clean up potential trailing slash or whitespace
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        resp = requests.get(api_url, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            # pushed_at is usually better for "last active" than updated_at (which changes on metadata updates)
            pushed_at = data.get("pushed_at")
            if pushed_at:
                # Convert "2024-01-16T12:00:00Z" to "2024-01-16"
                return pushed_at.split("T")[0]
        else:
            print(f"Failed to fetch {repo}: {resp.status_code}")
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
    
    return None

def update_file_date(filepath):
    """Reads file, finds external_link, gets date, and updates the date field."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find external_link
        link_match = re.search(r"^external_link:\s*(.+)$", content, re.MULTILINE)
        if not link_match:
            print(f"No external_link found in {filepath}")
            return
        
        repo_url = link_match.group(1).strip()
        new_date = get_repo_date(repo_url)
        
        if new_date:
            # Replace date: YYYY-MM-DD
            # Regex to find date: ....-..-..
            new_content = re.sub(r"^date:\s*[\d-]+\s*$", f"date: {new_date}", content, flags=re.MULTILINE)
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {filepath} to {new_date}")
            else:
                print(f"No match/change for date in {filepath}")
        else:
            print(f"Could not determine date for {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if not GH_TOKEN:
        print("Warning: GH_TOKEN not set. API rate limits may apply or private repos may fail.")
    
    for relative_path in PROJECT_FILES:
        # Construct absolute path assuming run from root
        filepath = os.path.abspath(relative_path)
        if os.path.exists(filepath):
            update_file_date(filepath)
        else:
            print(f"File not found: {filepath}")
