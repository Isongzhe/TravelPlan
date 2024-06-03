from fastapi import FastAPI, Query
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging
from concurrent.futures import ProcessPoolExecutor
import asyncio

# 設置日志
logging.basicConfig(level=logging.INFO)  # 設置日誌的基本配置，日誌級別為INFO
logger = logging.getLogger(__name__)  # 獲取日誌記錄器

app = FastAPI()  # 創建一個FastAPI應用實例

executor = ProcessPoolExecutor(
    max_workers=5
)  # 創建一個ProcessPoolExecutor，最大進程數為5


def crawl_google_map_task(url: str):
    start_time = time.time()  # 記錄開始時間

    logger.info(f"Starting crawl for URL: {url}")  # 記錄開始抓取的URL

    # 启动 Edge 浏览器
    options = webdriver.EdgeOptions()  # 創建Edge瀏覽器選項
    # 暫時禁用無頭模式以進行調試
    options.add_argument("--headless")  # 無頭模式
    options.add_argument("--log-level=3")  # 設置日誌級別為 ERROR
    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options,  # 安裝並啟動Edge瀏覽器
    )

    try:
        driver.get(url)  # 瀏覽器打開指定的URL
        logger.info("Page loaded successfully")  # 記錄頁面成功加載

        # 等待目標元素加載完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wuvLZe.fontBodyMedium"))
        )

        # 獲取頁面內容
        page_source = driver.page_source  # 獲取頁面的HTML源代碼

        # 使用 BeautifulSoup 解析頁面內容
        soup = BeautifulSoup(page_source, "lxml")  # 使用BeautifulSoup和lxml解析HTML內容

        # 直接查找包含目標文本的 <div> 標籤
        target_div = soup.find(
            "div", class_="wuvLZe fontBodyMedium"
        )  # 查找包含目標文本的<div>標籤

        if target_div:
            h2_element = target_div.find("h2")  # 查找<div>中的<h2>標籤
            if h2_element:
                h2_text = h2_element.get_text()  # 獲取<h2>標籤的文本內容
                if "個地點" in h2_text:  # 如果文本內容包含“個地點”
                    total_places_text = h2_text  # 記錄包含總地點數的文本
                    total_places = int(
                        total_places_text.split("·")[1].split(" ")[0]
                    )  # 提取並轉換總地點數為整數
                    logger.info(f"Total places: {total_places}")  # 記錄總地點數
                else:
                    raise Exception("The h2 element does not contain the expected text")
            else:
                raise Exception("Unable to find the h2 element within the target div")
        else:
            raise Exception("Unable to find the target div element")

        # 找到滚动区域元素
        scrollable_div = driver.find_element(
            By.CLASS_NAME,
            "m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc",  # 使用class_name找到可滾動的div元素
        )
        logger.info("Scrollable div found")  # 記錄找到可滾動的div元素

        # 滚动加载更多景点
        scroll_count = max(0, (total_places - 20 + 19) // 20)  # 計算需要滾動的次數

        for _ in range(scroll_count):  # 循環滾動
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div,  # 使用JavaScript滾動到div的底部
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "fontHeadlineSmall.rZF81c")
                )
            )
            logger.info("Scrolled down to load more places")  # 記錄每次滾動
        time.sleep(1)  # 等待一秒
        # 獲取滾動後的頁面內容
        page_source = driver.page_source  # 再次獲取頁面的HTML源代碼
        soup = BeautifulSoup(
            page_source, "lxml"
        )  # 使用BeautifulSoup和lxml重新解析HTML內容

        # 获取景点名称
        places = []  # 初始化景點名稱列表
        place_elements = soup.find_all(
            "div", {"class": "fontHeadlineSmall rZF81c"}
        )  # 查找所有景點名稱的div元素
        for place_element in place_elements:  # 遍歷所有景點名稱的div元素
            places.append(place_element.get_text())  # 添加景點名稱到列表中
        logger.info(f"Total places found: {len(places)}")  # 記錄找到的景點總數

        end_time = time.time()  # 記錄結束時間
        processing_time = end_time - start_time  # 計算處理時間

        return {
            "scroll_count": scroll_count,
            "total_places": total_places,
            "scrapped_total_places": len(places),
            "places_name": places,
            "processing_time": processing_time,
        }  # 返回結果

    except Exception as e:  # 捕獲異常
        logger.error(f"An error occurred: {e}")  # 記錄錯誤
        return {"error": str(e)}  # 返回錯誤信息

    finally:
        driver.quit()  # 關閉瀏覽器
        logger.info("Driver quit")  # 記錄瀏覽器已關閉


@app.get("/crawl_google_map")
async def crawl_google_map(
    url: str = Query(..., description="URL of the Google Map to crawl"),
):
    loop = asyncio.get_event_loop()  # 獲取當前事件循環
    result = await loop.run_in_executor(
        executor, crawl_google_map_task, url
    )  # 在執行器中運行同步任務
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # 啟動FastAPI應用
