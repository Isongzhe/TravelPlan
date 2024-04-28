from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import googlemaps
import json

def scrape_url(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--enable-features=SameSiteByDefaultCookies")
    options.add_argument("--log-level=3")
    driver = webdriver.Edge(options=options)
    url = "https://maps.app.goo.gl/zLPNc4hTaYNBmG3n8"
    driver.get(url)
    time.sleep(0.1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sights = soup.find_all('div', {'class': 'm6QErb'})
    seen = set()
    places = {}

    for sight in sights:
        sight_name = sight.find('div', {'class': 'fontHeadlineSmall rZF81c'})
        if sight_name is not None:
            name = sight_name.text
            if name not in seen:
                seen.add(name)
                rating = sight.find('span', {'class': 'UY7F9'}).text
                # 移除括號和逗號，然後轉換為整數
                rating = int(rating[1:-1].replace(',', ''))
                # 將地點名稱和評論數存入字典
                places[name] = rating
    driver.quit()
    return places


def get_place_info(place_name, expected_rating):
    gmaps = googlemaps.Client(key='AIzaSyBr0uayIFWpufzzq-hxl2p8-B4nYLxTSN0')        
    result = gmaps.places(place_name)
    if result['status'] == 'OK' and result['results']:
        place = result['results'][0]
        api_rating = place.get('user_ratings_total')
        if api_rating == expected_rating:
            return {
                'original_name': place_name,
                'name': place['name'],
                'address': place['formatted_address'],
                'location': place['geometry']['location'],
                'types': place['types'],
            }
        else:
            return f"{place_name} 的評論數 {api_rating} 與期望的評論數 {expected_rating} 不符。"
    else:
        return f"{place_name} 沒有找到結果。"

# places = scrape_url("https://maps.app.goo.gl/zLPNc4hTaYNBmG3n8")
# for place_name, rating in places.items():
#     result = get_place_info(place_name, rating)
#     # 將結果轉換為 JSON 字串
#     json_results = json.dumps(result, ensure_ascii=False, indent=4)
#     print(json_results)