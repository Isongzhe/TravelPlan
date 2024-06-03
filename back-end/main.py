import asyncio
from fastapi import FastAPI, Query
from pyppeteer import launch
from bs4 import BeautifulSoup
import time
import logging

# 設置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# 指定 Microsoft Edge 的可執行文件路徑
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 最大并发数
MAX_CONCURRENT_TASKS = 5

# 创建信号量来限制并发数
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


async def crawl_google_map_task(url: str):
    async with semaphore:
        start_time = time.time()
        logger.info(f"Starting crawl for URL: {url}")

        browser = await launch(
            headless=True,
            executablePath=edge_path,
        )
        page = await browser.newPage()

        try:
            await page.goto(url)
            logger.info("Page loaded successfully")

            await page.waitForSelector(
                ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc", timeout=10000
            )

            previous_height = await page.evaluate(
                """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight"""
            )
            while True:
                await page.evaluate(
                    """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollBy(0, document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight)"""
                )
                await asyncio.sleep(1)  # 使用 asyncio.sleep 代替 page.waitFor
                new_height = await page.evaluate(
                    """document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ussYcc").scrollHeight"""
                )
                if new_height == previous_height:
                    break
                previous_height = new_height
                logger.info("Scrolled down to load more places")

            page_source = await page.content()

            soup = BeautifulSoup(page_source, "lxml")

            places = []
            place_elements = soup.find_all("div", {"class": "fontHeadlineSmall rZF81c"})
            for place_element in place_elements:
                places.append(place_element.get_text())
            logger.info(f"Total places found: {len(places)}")

            end_time = time.time()
            processing_time = end_time - start_time

            return {
                "scrapped_total_places": len(places),
                "places_name": places,
                "processing_time": processing_time,
            }

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {"error": str(e)}

        finally:
            await browser.close()
            logger.info("Task completed.")


@app.get("/crawl_google_map")
async def crawl_google_map(
    url: str = Query(..., description="URL of the Google Map to crawl"),
):
    result = await asyncio.gather(crawl_google_map_task(url))
    return result[0]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
