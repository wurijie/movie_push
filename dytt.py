#--*-- encoding :UTF-8 --*--
import requests
from bs4 import BeautifulSoup
import re

class dytt():
    def __init__(self):
        self.index_url = "http://www.dytt8.net"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        self.headers = {
            'User-Agent': user_agent
        }
        self.s = requests.session()
        self.error = 0

    def getDownloadUrl(self, url):
        r = self.s.get(url)
        r.encoding = "gb2312"

        con = BeautifulSoup(r.text, "html.parser")
        a = con.select("#Zoom span table tbody tr td a")

        if a:
            return a[0].text
        #如果返回的数据里缺少下载地址，则重试3次
        else:
            self.error += 1

            if self.error < 3:
                self.getDownloadUrl(url)
            else:
                self.error = 0

    def getMovies(self):
        r = self.s.get(url=self.index_url, headers=self.headers)
        r.encoding="gb2312"

        bs = BeautifulSoup(r.text, "html.parser")

        contents = bs.select(".co_content8")
        target_tds = contents[0].select("td")

        resultArr = []
        for td in target_tds:
            td_a = td.select("a")
            if len(td_a):
                name = td_a[1].text
                name = re.search(r"《(.+)》", name).groups()[0]
                href = self.index_url + td_a[1].get("href")

                download_url = self.getDownloadUrl(href)

                obj = {"name": name, "href": download_url, "from": "电影天堂"}
                resultArr.append(obj)

        return resultArr