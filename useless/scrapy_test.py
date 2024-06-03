from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 WebDriver（假設使用的是 Chrome）
driver = webdriver.Chrome()

# 打開目標頁面
driver.get("https://maps.app.goo.gl/5JyZocb8bVodWVX76")

# 使用顯性等待
wait = WebDriverWait(driver, 10)  # 最多等待10秒
try:
    total_places_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h2[@data-relingo-block='true']"))
    )
    logger.info("Total places element found")

    total_places_text = total_places_element.text
    total_places = int(total_places_text.split("·")[1].split(" ")[0])
    logger.info(f"Total places: {total_places}")

except Exception as e:
    logger.error(f"An error occurred: {e}")

finally:
    driver.quit()
