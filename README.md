# Reddit News Summarizer

A powerful tool that scrapes the latest news from the **r/artificial** subreddit, summarizes the top stories using Google's **Gemini AI**, and presents them in a clean, modern web dashboard.

## Features

- **Reddit Scraper**: Fetches top posts and comments from r/artificial within the last 24 hours.
- **AI Summarization**: Uses Gemini 1.5 Flash to analyze and summarize the most important news items.
- **Web Dashboard**: A responsive React/Vite application to view the summarized news tiles.
- **AWS Integration**: Designed to run on AWS Lambda with S3 storage for daily automated updates.

## Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Google Gemini API Key**

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ar-international/reddit-news-summarizer.git
cd reddit-news-summarizer
```

### 2. Backend Setup
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

Set up your environment variable for the Gemini API key:
- On Windows (PowerShell): `$env:GEMINI_API_KEY="your_api_key_here"`
- On Linux/Mac: `export GEMINI_API_KEY="your_api_key_here"`

### 3. Frontend Setup
Navigate to the dashboard directory and install dependencies:
```bash
cd dashboard
npm install
```

## Usage

### Running Locally

1. **Generate News Summary**:
   Run the main script to scrape Reddit and generate the `news_summary.json`:
   ```bash
   python main.py
   ```

2. **Start the Dashboard**:
   Start the Vite development server:
   ```bash
   cd dashboard
   npm run dev
   ```
   Open your browser at `http://localhost:5173` to view the dashboard.

## Deployment

This project includes an AWS SAM template (`template.yaml`) for deploying the scraper and analyzer as a scheduled Lambda function.

```bash
sam build
sam deploy --guided
```
