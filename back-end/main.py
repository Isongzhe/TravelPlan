from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/results")
def read_results():
    file_path = 'D:\\GitHub\\TravelPlan\\back-end\\results.json'
    if not os.path.isfile(file_path):
        return {"error": f"File not found: {file_path}"}
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"404 not found": str(e)}