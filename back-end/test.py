import os

from googlemaps import Client, places

# 將 YOUR_API_KEY 替換為你的 Google Maps API 金鑰
gmaps = Client(key="AIzaSyBr0uayIFWpufzzq-hxl2p8-B4nYLxTSN0")

# 設定搜尋條件
search_text = "Animate 秋葉原店"
language_code = "zh-tw"
fields = ["place_id", "name", "geometry", "user_ratings_total", "types"]

# 發送搜尋請求
response = gmaps.places(query=search_text, language=language_code)

# 檢查回應狀態
if response["status"] == "OK":
    # 顯示搜尋結果
    for place in response["results"]:
        print(f"名稱: {place['name']}")
        print(f"地點 ID: {place['place_id']}")
        print(f"經緯度: {place['geometry']['location']}")
        print(f"評分總數: {place.get('user_ratings_total', 'N/A')}")
        print(f"類型: {', '.join(place['types'])}\n")
else:
    print(f"搜尋失敗: {response['status']}")
