import requests
import json


# url = "https://navitime-route-totalnavi.p.rapidapi.com/route_transit"

# days = "10"
# start = {"lat": 35.7768,"lon": 140.3181}
# goal = {"lat": 35.6706,"lon": 139.7528}
# payment = "ic"
# start_time = "2022-01-19T10:00:00"
# term = "1440"
# limit = "5"
# datum = "wgs84"
# coord_unit = "degree"

# querystring = {
#     "days": days,
#     "start": json.dumps(start),
#     "goal": json.dumps(goal),
#     "payment": payment,
#     "start_time": start_time,
#     "term": term,
#     "limit": limit,
#     "datum": datum,
#     "coord_unit": coord_unit
# }


# headers = {
# 	"X-RapidAPI-Key": "e8351ada85mshf8beb48bb2c6ce5p198a89jsnf265c730e4ed",
# 	"X-RapidAPI-Host": "navitime-route-totalnavi.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=4))
with open(r'back-end\route_response.json') as f:
    response = json.load(f)
    
# summary = response.json()['items'][1]['summary']
move_types = [item['summary']['move']['move_type'] for item in response['items']]
summaries = [item['summary'] for item in response['items']]
print(move_types)

'''
根據你的需求，以下可能是重要的信息：

no: 路線的編號。
start 和 goal: 分別表示起點和終點的座標和名稱。
move:
transit_count: 轉乘次數。
walk_distance: 步行距離。
fare: 車費，包括不同的單位價格。
from_time 和 to_time: 出發和到達時間。
time: 總旅行時間。
distance: 總旅行距離。
move_type: 旅行方式，例如地方火車、快速火車、超快速火車和步行。
這些信息可能對於理解和規劃路線非常有用。然而，哪些信息是重要的，取決於你的具體需求。
'''


# 遍歷所有的項目
for item in response['items']:
    # 獲取時間
    time = item['summary']['move']['time']
    # 獲取轉乘次數
    transit_count = item['summary']['move']['transit_count']
    # 獲取步行距離
    distance = item['summary']['move']['distance']
    # 檢查 'fare' 是否存在，如果存在則獲取車費，否則設為 '未知'
    fare = item['summary']['move']['fare']['unit_0'] if 'fare' in item['summary']['move'] else 0
    # 打印出時間、車費、轉乘次數和步行距離
    print(f"路線 {item['summary']['no']}：時間 {time} 分鐘，車費 {fare} 日元，轉乘次數 {transit_count} 次，步行距離 {distance} 米。")

def handle_point_section(section):
    coord = section['coord']
    name = section['name']
    print(f'Point: {name}, 座標: {coord}')
    if section.get('node_types') is not None:
        route_symbols = section['numbering']['departure']
        for route_symbol in route_symbols:
            print(f'路線代號: {route_symbol['symbol']}{route_symbol['number']}')
        if section.get('gateway') is not None:
            print(f'車站入口: {section['gateway']}')

def handle_move_section(section):
    move_type = section['move']
    time = section['time']
    distance = section['distance']
    print(f'移動方式: {section['line_name']}, 時間:{time}分鐘, 距離: {distance}米\n')
    if move_type == 'local_train':
        transport = section['transport']
        fare = transport['fare']['unit_0']
        line_name = section['line_name']
        print(f'搭乘線路: {line_name}, 費用為: {fare}\n')

# 假設 route 是你想要查看的路線
route = response['items'][0]['sections']
for route_section in route:
    if route_section['type'] == 'point':
        handle_point_section(route_section)
    elif route_section['type'] == 'move':
        handle_move_section(route_section)

# # 獲取路線的所有路線段
# for section in route:
#     # 獲取路線段的類型
#     section_type = section['type']
#     # 如果路線段的類型是 'move'，則解析相關的信息
#     if section_type == 'move':
#         # # 獲取車費
#         # fare = section['transport']['fare']['unit_0']
#         # 獲取時間
#         time = section['time']
#         # 獲取距離
#         distance = section['distance']
#         # 獲取路線名稱
#         line_name = section['line_name']
#         # 打印出車費、時間、距離和路線名稱
#         print(f"路線名稱：{line_name}，車費：{fare}，時間：{time}，距離：{distance}")
#     # 如果路線段的類型是 'point'，則解析相關的信息
#     elif section_type == 'point':
#         # 獲取站點名稱
#         station_name = section['name']
#         route_symbol = section['numbering']['departure']
#         # 打印出站點名稱
#         print(f"站點名稱：{station_name}，代號為{route_symbol['symbol']}{route_symbol['number']}")