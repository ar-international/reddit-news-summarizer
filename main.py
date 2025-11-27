import json
import os
import boto3
from scraper import fetch_reddit_posts, filter_posts_last_24h, simplify_data
from analyzer import analyze_with_gemini

s3 = boto3.client('s3')


def upload_to_s3(data, bucket_name, key):
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        print(f"Successfully uploaded {key} to {bucket_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def lambda_handler(event, context):
    print("Starting Reddit AI News Scraper Lambda...")
    
    # 1. Fetch Data
    print("Fetching posts from r/artificial...")
    raw_data = fetch_reddit_posts(limit=50)
    
    if not raw_data:
        print("Failed to fetch data.")
        return {"statusCode": 500, "body": "Failed to fetch data from Reddit"}

    # 2. Filter Data
    print("Filtering posts from the last 24 hours...")
    recent_posts = filter_posts_last_24h(raw_data)
    print(f"Found {len(recent_posts)} posts from the last 24 hours.")
    
    if not recent_posts:
        print("No recent posts found.")
        return {"statusCode": 200, "body": "No recent posts found"}

    # 3. Simplify and Fetch Comments
    print("Fetching comments and simplifying data...")
    simplified_data = simplify_data(recent_posts)
    
    # 4. Analyze with Gemini
    print("Sending data to Gemini for analysis...")
    analysis_result = analyze_with_gemini(simplified_data)
    
    # 5. Post-process: Add URLs back
    if analysis_result:
        print("Adding URLs to summary...")
        for item in analysis_result:
            idx = item.get("original_index")
            if idx is not None and isinstance(idx, int) and 0 <= idx < len(simplified_data):
                item["url"] = simplified_data[idx].get("url")
            # Remove original_index to clean up output
            item.pop("original_index", None)

    # 6. Upload Results to S3
    if analysis_result:
        bucket_name = os.environ.get("S3_BUCKET_NAME")
        if bucket_name:
            # Use current date in filename to avoid overwriting if run multiple times or for history
            # But user asked for "upload news_summary.json", implying a static name or maybe daily overwrite.
            # Let's do a static name for now as requested, or maybe a date prefix?
            # User said "upload news_summary.json to S3 once obtained on given day".
            # I will use a date-stamped key for history and maybe a 'latest' key?
            # Let's stick to a simple key for now as per request, maybe with date.
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            key = f"news_summary_{date_str}.json"
            
            upload_to_s3(analysis_result, bucket_name, key)
            
            # Also upload as 'latest' for easy access?
            upload_to_s3(analysis_result, bucket_name, "news_summary_latest.json")
            
        else:
            print("S3_BUCKET_NAME environment variable not set. Saving locally.")
            with open("news_summary.json", "w", encoding="utf-8") as f:
                json.dump(analysis_result, f, indent=2)
            print(f"Analysis complete! Results saved to news_summary.json")
            print(json.dumps(analysis_result, indent=2))
            
        return {
            "statusCode": 200,
            "body": json.dumps("Analysis complete and uploaded to S3")
        }
    else:
        print("Analysis failed or returned no results.")
        return {
            "statusCode": 500,
            "body": "Analysis failed"
        }

if __name__ == "__main__":
    # Local testing simulation
    lambda_handler(None, None)
