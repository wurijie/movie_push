#--*-- encoding: UTF-8 --*--
import requests
from bs4 import  BeautifulSoup
import time

class seehd():
    def __init__(self):
        self.index_url = "http://www.seehd.so"
        self.headers = {
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        }
        self.errors = 0
        self.request_result = ""

    #网络请求专用工具
    def request_tool(self):
        try:
            r = requests.get(self.index_url, headers = self.headers)
            r.encoding = "utf-8"
            self.request_result = r.text
            return True
        except:
            return False

    #获取电影数据
    def getMovies(self):
        #尝试三次请求网站数据，若都不成功则返回空[]
        self.errors = 0
        while not self.request_tool():
            if self.errors > 3:
                print("刷了3次seeHD都失败了，下次再来！")
                return []
            else:
                self.errors += 1

            time.sleep(5) #休息5s


        content = BeautifulSoup(self.request_result, "html.parser")
        html_titles = content.select("#J_posts_list tr .subject .title")

        if html_titles:
            resultArr = []
            for title in html_titles:
                # 只抓取最新的影片
                type = title.select("a:nth-of-type(2)")[0].string
                if not type == "[网友分享电影]":
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
