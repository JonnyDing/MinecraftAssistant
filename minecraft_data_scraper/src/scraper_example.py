import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random

# 日志输出
def log_message(message):
    print(f"[INFO] {message}")

# 随机延迟函数，避免被反爬
def random_sleep(min_time=2, max_time=5):
    time_to_sleep = random.uniform(min_time, max_time)
    time.sleep(time_to_sleep)

# 初始化浏览器
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# 爬取正文文本
def scrape_content(url):
    log_message(f"开始爬取页面：{url}")
    driver = init_driver()
    driver.get(url)
    random_sleep(3, 6)

    try:
        # 等待页面的主要内容加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Mid2L_con"))
        )

        # 定位到整个内容容器
        content_container = driver.find_element(By.CSS_SELECTOR, "div.Mid2L_con")

        # 提取所有 <p> 标签内容
        paragraphs = content_container.find_elements(By.TAG_NAME, "p")
        full_text = ""
        for p in paragraphs:
            text = p.text.strip()  # 去除空白内容
            if text:  # 跳过空白段落
                full_text += text + "\n"

        log_message("成功爬取所有正文文本。")
        return full_text.strip()

    except Exception as e:
        log_message(f"爬取失败，错误信息：{e}")
        return None

    finally:
        driver.quit()

# 保存数据到 TXT 文件
def save_to_txt(content, output_file="data/raw_data/output.txt"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 确保目录存在
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    log_message(f"数据已保存到 {output_file}")

# 主函数
if __name__ == "__main__":
    for i in range(68):
        url = f"https://www.gamersky.com/handbook/201607/777466_{i+1}.shtml"
        output_path = f"../data/raw_data/output{i+1}.txt"
        content = scrape_content(url)
        if content:
            save_to_txt(content, output_file=output_path)
        else:
            log_message("未能获取到有效内容，程序结束。")
