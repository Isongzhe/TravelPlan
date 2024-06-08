import asyncio
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse

# 引入 scrapy_list.py 中的函式，並使用別名
from scrapy_list import (
    crawl_google_map as scrapy_crawl_google_map,
)

from typing import Dict, List
import googlemaps
from googlemaps.places import places

# 創建 FastAPI 應用
app = FastAPI()


# 創建 api/crawl_google_map 路由，使用 GET 方法，接收 URL 參數，並返回爬取結果
@app.get("/api/crawl_google_map")
async def crawl_google_map(
    # 使用 Query 來接收 URL 參數，語法: Query(參數類型, 參數描述, 參數默認值)，... 代表必填參數
    url: str = Query(..., description="URL of the Google Map to crawl"),  # 接收參數
) -> Dict:  # 加入回傳值類型提示
    try:
        # 使用 asyncio.create_task 創建並發任務
        task = asyncio.create_task(scrapy_crawl_google_map(url))  # 併發任務
        result = await task  # 結果等待任務完成
        return result
    except Exception as e:
        # 詳細記錄錯誤訊息
        print(f"爬取 Google Map 發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"爬取 Google Map 發生錯誤: {e}")


GOOGLE_API_KEY = "AIzaSyBr0uayIFWpufzzq-hxl2p8-B4nYLxTSN0"  # 請替換成你的 API 金鑰
# 創建 Google Maps 客戶端
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


# 定義異步任務，用於搜索每個單一地點
async def _search_google_place(text: str) -> Dict:
    """發送單一地點請求到 Google Places API 並返回結果。"""
    try:
        # 使用 'places' 函數進行地點搜索
        response = gmaps.places(
            query=text,  # 搜尋文字
            language="zh-TW",  # 語言代碼
        )

        # 檢查回應狀態，並確保至少有一個候選地點
        if response["status"] == "OK" and response["results"]:
            # 直接取第一個地點作為搜索結果(未來要改進，應該要篩選用戶真正的期望搜尋結果)
            place = response["results"][0]

            # 從回應中提取地點資料
            place_data = {
                "place_id": place.get("place_id"),
                "name": place.get("name"),
                "geometry": place.get("geometry")["location"],
                "user_ratings_total": place.get("user_ratings_total"),
                "types": place.get("types"),
            }

            return place_data  # 返回整理好的地點資料
        else:
            # 詳細記錄錯誤訊息，包含搜尋的文字
            print(f"Google Places API 請求失敗: 未找到地點 {text}")
            # 拋出 HTTPException，狀態碼 404 表示找不到資源
            raise HTTPException(status_code=404, detail=f"搜尋地點 {text} 時發生錯誤")

    except Exception as e:
        # 詳細記錄錯誤訊息，包含錯誤物件
        print(f"Google Places API 請求失敗: {e}")
        # 拋出 HTTPException，狀態碼 500 表示伺服器內部錯誤
        raise HTTPException(status_code=500, detail=f"搜尋地點 {text} 時發生錯誤")


# 創建 api/place_info 路由，使用 POST 方法，接收 JSON 請求體，並返回地點資訊
@app.post("/api/place_info")
async def search_google_places(request: Request):
    """使用 Google Places API 搜尋地點。"""
    try:
        # 從POST中的，請求體中取得 JSON 資料
        body = await request.json()
        # 從JSON中，解析取得地點名稱列表
        places_name = body.get("places_name")
        # 檢查地點名稱列表是否有效
        if not places_name or not isinstance(places_name, list):
            # 拋出 HTTPException，狀態碼 400 表示請求格式錯誤
            raise HTTPException(
                status_code=400, detail="請求體中需要包含 'places_name' 列表"
            )

        # 使用 asyncio.gather 同時發送所有請求
        tasks = [_search_google_place(place) for place in places_name]
        # 等待所有請求完成，並將結果儲存到 places_data 列表中
        places_data: List[Dict] = await asyncio.gather(*tasks)

        # 返回 JSON 格式的回應，包含所有地點的資料
        return JSONResponse(content=places_data)
    except HTTPException as e:
        # 如果發生 HTTPException，則返回 JSON 格式的錯誤訊息和對應的狀態碼
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


if __name__ == "__main__":
    import uvicorn

    # 運行 uvicorn 伺服器，監聽所有網路介面 (0.0.0.0) 的 8000 埠，並啟用自動重新載入
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
