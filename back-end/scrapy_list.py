import asyncio
import time
import logging
from typing import Dict

from pyppeteer import launch
from bs4 import BeautifulSoup

# 設置日誌
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# 獲取日誌記錄器
logger = logging.getLogger(__name__)

# 指定 Microsoft Edge 的可執行文件路徑
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 最大並發數
MAX_CONCURRENT_TASKS = 3

# 創建信號量來限制併發數
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


# 定義異步任務
async def crawl_google_map(url: str) -> Dict:
    """爬取 Google 地圖地點資訊。

    Args:
        url: Google 地圖網址。

    Returns:
        包含爬取結果的字典，包含地點數量、地點名稱和處理時間。
    """
    # 使用 semaphore 來限制併發數，同時最多只有 3 個爬蟲任務在運行
    async with semaphore:
        start_time = time.time()  # 記錄任務開始時間

        # 日誌記錄任務開始時間
        logger.info(f"Starting crawl for URL: {url} at {start_time}")
        # 使用 pyppeteer 創建瀏覽器
        browser = await launch(
            headless=True,  # 開啟無頭模式(不顯示瀏覽器視窗)
            executablePath=edge_path,  # 指定 Microsoft Edge 的可執行文件路徑
        )
        page = await browser.newPage()

        try:
            # 訪問頁面
            await page.goto(url)
            logger.info("Page loaded successfully")

            # 等待地點元素加載
            await page.waitForSelector(
                ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc", timeout=5000
            )
            # 獲取頁面高度，以便清單滾動到底部
            previous_height = await page.evaluate(
                """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight"""
            )

            # 設置最大滾動次數以防止無限滾動
            max_scrolls = 4  # 最多4次滾動底部，最多100個地點
            scroll_count = 0  # 初始滾動次數
            # 滾動頁面以加載更多地點
            while scroll_count < max_scrolls:
                # 使用 page.evaluate 在瀏覽器中執行 JavaScript 代碼，來滾動頁面
                await page.evaluate(
                    """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollBy(0, document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight)"""
                )
                # 使用 asyncio.sleep 代替 page.waitFor，保持代碼的同步性
                await asyncio.sleep(1)  # 等待1秒
                # 獲取新的頁面高度
                new_height = await page.evaluate(
                    """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight"""
                )
                # 如果新的頁面高度等於上一次的高度，則說明已經滾動到底部，彈回載入，則退出循環
                if new_height == previous_height:
                    break
                # 更新上一次的頁面高度
                previous_height = new_height
                # 滾動次數加1
                scroll_count += 1
                # 日誌記錄滾動次數
                logger.info(
                    f"Scrolled down to load more places (scroll count: {scroll_count})"
                )
            # 獲取頁面內容
            page_source = await page.content()
            # 使用 BeautifulSoup 解析頁面內容
            soup = BeautifulSoup(page_source, "lxml")
            # 獲取所有地點元素
            places = []  # 存儲地點名稱
            place_elements = soup.find_all("div", {"class": "fontHeadlineSmall rZF81c"})
            # 歷遍提取地點名稱
            for place_element in place_elements:
                places.append(place_element.get_text())  # 加回地點名稱到places最後

            # 日誌記錄找到的地點數量
            logger.info(f"Total places found: {len(places)}")
            end_time = time.time()  # 任務結束時間
            processing_time = end_time - start_time  # 計算任務處理時間
            # 日誌記錄任務完成時間
            logger.info(
                f"Completed crawl for URL: {url} at {end_time}, processing time: {processing_time}"
            )
            # 返回結果
            return {
                "scrapped_total_places": len(places),  # 回傳地點數量
                "places_name": places,  # 回傳地點名稱
                "processing_time": processing_time,  # 回傳處理時間
            }
        # 捕獲異常
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {"error": str(e)}
        # 最後執行的代碼塊，無論是否發生異常
        finally:
            await browser.close()  # 關閉瀏覽器
            logger.info("Task completed.")  # 日誌記錄任務完成
