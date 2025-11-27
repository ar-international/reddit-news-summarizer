import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)

def analyze_with_gemini(data):
    """
    Sends the simplified Reddit data to Gemini for analysis.
    """
    configure_gemini()
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = """
    You are an AI news analyst. I will provide you with a JSON containing recent posts and comments from r/artificial.
    
    Your task is to:
    1. Analyze the content of the posts and comments.
    2. Identify the top 5 most important AI news items or discussions.
    3. For each item, provide a title, a brief explanation (2-5 sentences), and the index of the original post in the input list.
    
    Input Data:
    {data}
    
    Output Format (JSON):
    [
        {{
            "rank": 1,
            "original_index": 0,
            "title": "Title of the news",
            "explanation": "Brief explanation..."
        }},
        ...
    ]
    
    Return ONLY the valid JSON array. Do not include markdown formatting like ```json ... ```.
    """
    
    try:
        # Convert data to string for the prompt
        data_str = json.dumps(data, indent=2)
        final_prompt = prompt.format(data=data_str)
        
        response = model.generate_content(final_prompt)
        
        # Clean up response text if it contains markdown code blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text)
    except Exception as e:
        print(f"Error during Gemini analysis: {e}")
        return []
