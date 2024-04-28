from fastapi import FastAPI
import sys
sys.path.append('D:\\GitHub\\TravelPlan\\back-end\\')
from method.scrape import scrape_url, get_place_info
import time



app = FastAPI()
# python -m uvicorn main:app --reload :啟動伺服器

# https://maps.app.goo.gl/zLPNc4hTaYNBmG3n8
@app.get("/api/scrape")
async def scrape(url: str):
    start_time = time.time()

    places = scrape_url(url)
    results = []
    for place_name, rating in places.items():
        result = get_place_info(place_name, rating)
        results.append(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return results