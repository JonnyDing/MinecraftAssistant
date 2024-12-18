import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# 设置目标URL
url = "https://www.mcmod.cn/item/list/1-1.html"

# 发送HTTP请求并获取网页内容
response = requests.get(url)
response.encoding = 'utf-8'  # 防止中文乱码
html_content = response.text

# 解析HTML内容
soup = BeautifulSoup(html_content, "html.parser")

# 初始化结果列表
data = []

# 找到所有<tr>行（每行包含分类标题和物品列表）
rows = soup.find_all("tr")

# 遍历每一行提取内容
for row in rows:
    # 提取分类标题（<th> 标签）
    category_th = row.find("th", class_="item-list-type-left")
    if category_th:
        category_name = category_th.get_text(strip=True)  # 获取分类名称

        # 提取对应的物品列表（<td> 标签内的 <ul><li>）
        item_td = row.find("td", class_="item-list-type-right")
        if item_td:
            items = item_td.find_all("li")  # 提取所有li标签
            for item in items:
                # 提取物品名称和链接
                item_link_tag = item.find("a")  # 提取a标签
                if item_link_tag:
                    item_name = item_link_tag.get_text(strip=True)
                    item_url = item_link_tag.get("href")
                    full_url = f"https://www.mcmod.cn{item_url}" if item_url else "无链接"

                    # 添加到结果列表
                    data.append({
                        "分类": category_name,
                        "物品名称": item_name,
                        "链接": full_url
                    })

# 将结果保存为Excel
df = pd.DataFrame(data)
excel_file = "../parser/item_list.xlsx"
df.to_excel(excel_file, index=False)
print(f"数据已保存到 Excel 文件: {excel_file}")

# 将结果保存为JSON
json_file = "../parser/item_list.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print(f"数据已保存到 JSON 文件: {json_file}")

# 打印部分结果
print("\n解析结果预览:")
print(df.head())
