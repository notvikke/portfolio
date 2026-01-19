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
    # GraphQL Query
    # limit repos to 100 for language stats. If user has > 100, we prioritize the top 100 most recently updated or we could page.
    # For simplicity and speed in a portfolio action, 100 is usually sufficient for "Most Used" approximation. 
    # But let's try to get total count correctly.
    
    query = """
    query {
      viewer {
        login
        repositories(first: 100, ownerAffiliations: [OWNER], isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
          totalCount
          nodes {
            name
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
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
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
    
    # 2. Most Used Language
    language_sizes = {}
    repos = data["repositories"]["nodes"]
    
    for repo in repos:
        if not repo["languages"]["edges"]:
            continue
        for edge in repo["languages"]["edges"]:
            lang_name = edge["node"]["name"]
            size = edge["size"]
            language_sizes[lang_name] = language_sizes.get(lang_name, 0) + size
            
    most_used_lang = "N/A"
    if language_sizes:
        most_used_lang = max(language_sizes, key=language_sizes.get)

    # 3. Total Contributions (Last Year)
    # totalContributions in calendar includes commits, issues, PRs, reviews, etc.
    total_contributions = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    
    # 4. Current Streak
    calendar_weeks = data["contributionsCollection"]["contributionCalendar"]["weeks"]
    
    # Flatten days
    all_days = []
    for week in calendar_weeks:
        for day in week["contributionDays"]:
            all_days.append(day)
            
    # Sort by date descending just to be safe, though usually they are asc
    all_days.sort(key=lambda x: x["date"], reverse=True)
    
    current_streak = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Find start index (today or yesterday)
    # API might return future days if we are strictly checking "today" in UTC vs local.
    # We'll just look for the most recent day with contributions to start the streak if it's today or yesterday?
    # Strict streak: Streak is alive if you contributed today OR yesterday.
    
    # Let's simple iterate backwards
    streak_alive = True
    
    # Check if we have data for today
    has_contributed_today = False
    
    # Filter out future days just in case
    valid_days = [d for d in all_days if d["date"] <= today_str]
    
    if not valid_days:
        current_streak = 0
    else:
        # Check specific today/yesterday logic
        # For simplicity: count backwards from latest available day. 
        # If the gap between today and the last contribution is > 1 day, streak is 0.
        
        last_contribution_date_str = None
        
        for day in valid_days:
            if day["contributionCount"] > 0:
                last_contribution_date_str = day["date"]
                break
        
        if last_contribution_date_str:
            last_date = datetime.strptime(last_contribution_date_str, "%Y-%m-%d")
            today = datetime.strptime(today_str, "%Y-%m-%d")
            delta = (today - last_date).days
            
            if delta > 1:
                current_streak = 0
            else:
                # Streak is valid, count it
                # Logic: Count consecutive days > 0 starting from that last_date
                current_count = 0
                
                # Re-iterate or find index
                start_index = -1
                for i, day in enumerate(valid_days):
                    if day["date"] == last_contribution_date_str:
                        start_index = i
                        break
                
                # Check backwards (chronologically) from the start day?
                # valid_days is sorted DESC (newest first).
                # So we iterate forward in valid_days list
                
                # previous_date meant the "next day" in the loop (which is chronologically older)
                # We need to ensure continuity.
                
                current_ref_date = datetime.strptime(valid_days[start_index]["date"], "%Y-%m-%d")
                
                for i in range(start_index, len(valid_days)):
                    day = valid_days[i]
                    day_date = datetime.strptime(day["date"], "%Y-%m-%d")
                    expected_date = current_ref_date - timedelta(days=current_count)
                    
                    if day_date == expected_date:
                        if day["contributionCount"] > 0:
                            current_count += 1
                        else:
                            break
                    else:
                        # Missing a day in the list? (Shouldn't happen with grid) or we skipped a day that had 0?
                        # If we have 0 count at expected date, we stop.
                        # Wait, valid_days contains ALL days (including 0 count).
                         if day["contributionCount"] == 0:
                            break
                            
                current_streak = current_count
        else:
            current_streak = 0

    # Calculate Total LOC
    total_bytes = sum(language_sizes.values())
    total_loc = int(total_bytes / 40)

    stats = {
        "total_repos": total_repos,
        "most_used_lang": most_used_lang,
        "total_contributions": total_contributions, # formatted in frontend
        "current_streak": current_streak,
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
