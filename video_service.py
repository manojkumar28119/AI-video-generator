import requests
import os
from dotenv import load_dotenv

load_dotenv()

class VideoService:
    def __init__(self):
        print("[VIDEO_SERVICE] Initializing Video service...")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        if not self.pexels_api_key:
            print("[VIDEO_SERVICE] WARNING: PEXELS_API_KEY not found in environment variables")
        else:
            print("[VIDEO_SERVICE] Video service initialized successfully")
    
    async def fetch_video(self, search_query: str) -> dict:
        """Fetch video from Pexels API"""
        print(f"[VIDEO_SERVICE] Starting video search for query: '{search_query}'")
        
        
        try:
            print("[VIDEO_SERVICE] Sending request to Pexels API...")
            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": self.pexels_api_key},
                params={"query": search_query, "per_page": 1}
            )
            
            print(f"[VIDEO_SERVICE] Pexels API response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[VIDEO_SERVICE] ERROR: Pexels API returned status {response.status_code}")
                return {"error": f"Pexels API error: {response.status_code}"}
            
            data = response.json()
            print(f"[VIDEO_SERVICE] Pexels API response data keys: {list(data.keys())}")
            
            if data.get("videos"):
                video_count = len(data["videos"])
                print(f"[VIDEO_SERVICE] Found {video_count} video(s)")
                
                video_url = data["videos"][0]["video_files"][0]["link"]
                video_id = data["videos"][0].get("id", "unknown")
                
                print(f"[VIDEO_SERVICE] Selected video ID: {video_id}")
                print(f"[VIDEO_SERVICE] Video URL: {video_url[:50]}...")
                
                return {
                    "success": True,
                    "video_url": video_url,
                    "video_id": video_id,
                    "total_found": video_count
                }
            else:
                print("[VIDEO_SERVICE] No videos found for the search query")
                return {"error": "No video found"}
                
        except Exception as e:
            print(f"[VIDEO_SERVICE] ERROR: Failed to fetch video - {str(e)}")
            return {"error": f"Video fetch failed: {str(e)}"}