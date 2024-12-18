import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
import time

# 输入文件路径
input_file = "../parser/item_list.xlsx"  # 输入的Excel文件路径
output_dir = "../data/resource_data"  # 输出的TXT文件夹路径

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


# 随机延迟函数
def random_sleep(min_time=2, max_time=5):
    sleep_time = random.uniform(min_time, max_time)
    print(f"[INFO] 随机延迟: {sleep_time:.2f} 秒")
    time.sleep(sleep_time)


# 重试机制函数
def fetch_with_retries(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"[WARN] 请求失败，重试 {attempt + 1}/{retries}: {e}")
            random_sleep(2, 5)  # 每次重试前延迟
    return None


# 加载 Excel 文件
data = pd.read_excel(input_file)

# 遍历每个链接进行爬取
for index, row in data.iterrows():
    name = row["物品名称"].replace("/", "_")  # 替换非法文件名字符
    url = row["链接"]
    output_path = os.path.join(output_dir, f"{name}.txt")  # 保存路径

    print(f"[INFO] 正在爬取: {name} ({url})")
    try:
        # 请求网页内容
        response = fetch_with_retries(url)
        if response is None:
            raise Exception("重试失败，无法获取网页内容。")

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 提取目标文本内容
        content_div = soup.find("div", class_="item-content common-text font14")
        if content_div:
            paragraphs = content_div.find_all("p")
            full_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        else:
            full_text = "未找到对应内容"

        # 保存内容到 TXT 文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"[SUCCESS] 已保存: {output_path}")

    except Exception as e:
        print(f"[ERROR] 爬取失败: {name}，错误信息: {e}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("爬取失败")

    # 随机延迟，模拟人工操作
    random_sleep(3, 6)

print(f"[INFO] 所有内容已保存到文件夹: {output_dir}")
