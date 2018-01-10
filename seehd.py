#--*-- encoding: UTF-8 --*--
import requests
from bs4 import  BeautifulSoup

class seehd():
    def __init__(self):
        self.s = requests.session()
        self.index_url = "http://www.seehd.so"
        self.headers = {
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        }

    def getMovies(self):
        r = self.s.get(self.index_url, headers=self.headers)

        content = BeautifulSoup(r.text, "html.parser")
        html_titles = content.select("#J_posts_list tr .subject .title")

        if html_titles:
            resultArr = []
            for title in html_titles:
                # 只抓取最新的影片
                type = title.select("a:nth-of-type(2)")[0].string
                if not type == "[新片分享]":
                    continue

                #优化电影名称
                html_a = title.select("a:nth-of-type(3)")[0]
                href = html_a.get("href")
                name = html_a.string.split(" ")[0]

                obj = {"name": name, "href": href, "from": "seeHD"}
                resultArr.append(obj)
            return resultArr
        else:
            return False
