from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import asyncio
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

app = FastAPI()

# Set up CORS middleware options
origins = [
    "http://localhost:5173",  # The origin you are making requests from, adjust as needed
    "http://localhost:3000",  # Add other origins as needed
    # You can use "*" to allow all origins, but be cautious with this approach
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def format_answer(answer):
    # Basic formatting can be expanded based on specific needs
    return answer.replace(" '", "'").replace(" ,", ",").replace(" .", ".").replace(" -", "-")

async def mock_send_post_request(url, json_data, headers):
    # Simulate network latency with asyncio.sleep
    await asyncio.sleep(2)  # 2 seconds delay
    # Return mock response
    return  "The sky appears blue because of a phenomenon called Rayleigh scattering. Blue light has shorter wavelengths than other colors in the visible spectrum, and it scatters more easily when it collides with particles or gas molecules in the atmosphere. This scattering effect causes blue light to be scattered in all directions throughout the sky, creating a blue appearance during the daytime hours. At sunrise and sunset, red light is more prominent due to its longer wavelength, which allows it to travel farther through the atmosphere without being scattered as much. This creates a reddish color in the sky."
    

class AIRequest(BaseModel):
    prompt: str

async def send_post_request(url, json_data, headers):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=headers) as response:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    return await response.json()
                else:
                    return await response.text()
    except aiohttp.ClientConnectorError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {e}")

@app.post("/generate-ai-response/")
async def generate_ai_response(request: AIRequest):
    url = "https://meta-llama-fast-api.p.rapidapi.com/mistralchat"
    payload = {"message": request.prompt}
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "meta-llama-fast-api.p.rapidapi.com"
    }

    # response = await send_post_request(url, payload, headers)
    print(f'{payload = }')
    response = await mock_send_post_request(url, payload, headers)
    print(f'{response  = } mistral')
    return response

# Define a new GET route for graph data
@app.get("/graph-data")
async def get_graph_data():
    # The mock data for the graph, matching the required structure
    graph_data = {
        "title": "Total Addressable Market (TAM)",
        "data": {
            "labels": ["2020", "2021", "2022", "2023"],
            "label": "Total Addressable Market",
            "values": [20, 30, 40, 50]  # Assuming these are in billions
        }
    }
    await asyncio.sleep(1)  # 1 seconds delay
    return graph_data

#Health Check Endpoint
@app.get("/health")
def read_health():
    return {"status": "healthy"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 6000)))