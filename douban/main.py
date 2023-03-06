# 豆瓣电影 Top 250 https://movie.douban.com/top250

import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

page_indexs = range(0, 250, 25)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


def download_all_htmls():
  htmls = []
  for idx in page_indexs:
    url = f"https://movie.douban.com/top250?start={idx}&filter="
    print('craw html:', url)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
      raise Exception('error')
    htmls.append(r.text)
  return htmls


def parse_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  article_items = soup.find(
      "div", class_="article").find(
      "ol", class_="grid_view").find_all(
      "div", class_="item")
  datas = []
  for article in article_items:
    rank = article.find("div", class_="pic").find("em").get_text()
    info = article.find("div", class_="info")
    title = info.find(
        "div", class_="hd").find(
        "span", class_="title").get_text()
    star = info.find(
        "div", class_="bd").find(
        "div", class_="star")
    rating_num = star.find("span", class_="rating_num").get_text()
    comments = star.find_all("span")[3].get_text()
    datas.append({
        "rank": rank,
        "title": title,
        "rating_num": rating_num,
        "comments": comments
    })
  return datas


all_datas = []
all_htmls = download_all_htmls()

for html in all_htmls:
  all_datas.extend(parse_html(html))

df = pd.DataFrame(all_datas)
df.to_excel("./output/豆瓣电影Top250.xlsx")
