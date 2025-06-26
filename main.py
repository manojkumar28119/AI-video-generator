from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gpt_service import GPTService
from video_service import VideoService
import datetime

print("[MAIN] Starting AI Video Generator API...")
print(f"[MAIN] Startup time: {datetime.datetime.now()}")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize services
print("[MAIN] Initializing services...")
gpt_service = GPTService()
video_service = VideoService()
print("[MAIN] All services initialized successfully")

class PromptInput(BaseModel):
    prompt: str

@app.post("/generate-video")
async def generate_video(data: PromptInput):
    request_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    print(f"\n[MAIN] ========== NEW REQUEST {request_id} ==========")
    print(f"[MAIN] Received prompt: '{data.prompt}'")
    
    try:
        # Step 1: Extract keywords using GPT
        print("[MAIN] Step 1: Starting keyword extraction...")
        keywords = await gpt_service.extract_keywords(data.prompt)
        search_query = ", ".join(keywords)
        print(f"[MAIN] Using search query: '{search_query}'")
        
        # Step 2: Fetch video from Pexels
        print("[MAIN] Step 2: Starting video search...")
        video_result = await video_service.fetch_video(search_query)
        
        if video_result.get("success"):
            print(f"[MAIN] SUCCESS: Video generation completed for request {request_id}")
            return {
                "video_url": video_result["video_url"],
                "keywords": keywords,
                "search_query": search_query,
                "request_id": request_id,
                "status_code": 200,
                "message": "Video generated successfully",
                "success": True,
            }
        else:
            print(f"[MAIN] PARTIAL SUCCESS: Keywords extracted but no video found for request {request_id}")
            return {
                "error": video_result.get("error", "No video found"),
                "keywords": keywords,
                "search_query": search_query,
                "request_id": request_id
            }
            
    except Exception as e:
        print(f"[MAIN] ERROR: Request {request_id} failed - {str(e)}")
        return {
            "error": f"Internal server error: {str(e)}",
            "request_id": request_id
        }
    finally:
        print(f"[MAIN] ========== END REQUEST {request_id} ==========\n")




#uvicorn main:app --reload # To run the server, use the command: