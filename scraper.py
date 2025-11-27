import requests
import time
from datetime import datetime, timedelta

def fetch_reddit_posts(subreddit="artificial", limit=25):
    """
    Fetches posts from a subreddit's new.json endpoint.
    """
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Reddit: {e}")
        return None

def filter_posts_last_24h(posts_data):
    """
    Filters posts to keep only those from the last 24 hours.
    """
    if not posts_data or 'data' not in posts_data or 'children' not in posts_data['data']:
        return []

    filtered_posts = []
    cutoff_time = datetime.now().timestamp() - (24 * 3600)

    for child in posts_data['data']['children']:
        post = child['data']
        if post['created_utc'] >= cutoff_time:
            filtered_posts.append(post)
            
    return filtered_posts

def fetch_comments(permalink):
    """
    Fetches comments for a specific post.
    """
    url = f"https://www.reddit.com{permalink}.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        time.sleep(1) # Be nice to Reddit API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Reddit returns a list: [post_listing, comment_listing]
        if len(data) >= 2:
            return data[1]['data']['children']
        return []
    except Exception as e:
        print(f"Error fetching comments for {permalink}: {e}")
        return []

def simplify_data(posts):
    """
    Simplifies the data structure for Gemini.
    """
    simplified = []
    
    # Limit to top 10 posts to avoid hitting rate limits or token limits too hard
    for post in posts[:10]:
        item = {
            "title": post.get("title"),
            "selftext": post.get("selftext"),
            "url": post.get("url"),
            "score": post.get("score"),
            "num_comments": post.get("num_comments"),
            "comments": []
        }
        
        # Fetch top 3 comments
        comments_data = fetch_comments(post['permalink'])
        for comment in comments_data[:3]:
            if 'data' in comment and 'body' in comment['data']:
                item["comments"].append(comment['data']['body'])
                
        simplified.append(item)
        
    return simplified
