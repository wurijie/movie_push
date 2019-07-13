#--*-- encoding :UTF-8 --*--
import requests
from bs4 import BeautifulSoup
import re
import time

class dytt():
    def __init__(self):
        self.index_url = "http://www.dytt8.net"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        self.headers = {
            'User-Agent': user_agent
        }
        self.errors = 0
        self.request_result = ""

    #用于发送网络请求
    def request_tool(self):
        try:
            r = requests.get(url=self.index_url, headers=self.headers)
            r.encoding = "gb2312"
            self.request_result = r.text
            return True
        except:
            return False

    #用于获取电影信息
    def getMovies(self):
        #请求三次服务器，若都失败，则跳过(返回空数组)
        self.errors = 0
        while not self.request_tool():
            if self.errors  > 3:
                print("刷了3次电影天堂都失败了，下次再来！")
                return []
            else:
                self.errors += 1

            time.sleep(5) #休息5s

        bs = BeautifulSoup(self.request_result, "html.parser")

        contents = bs.select(".co_content8")
        target_tds = contents[0].select("td")

        resultArr = []
        for td in target_tds:
            td_a = td.select("a")
            if len(td_a)>1:
                name = td_a[1].text
                name = re.search(r"《(.+)》", name).groups()[0]
                href = self.index_url + td_a[1].get("href")

                obj = {"name": name, "href": href, "from": "电影天堂"}
                resultArr.append(obj)

        return resultArr