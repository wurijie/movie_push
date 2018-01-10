#--*-- encoding: UTF-8 --*--
import requests
import seehd
import dytt
import hashlib
import time
import os

class movie_push():
    def __init__(self):
        #server酱推送地址
        self.ftqq_url = input("请输入server酱地址推送：(申请地址http://sc.ftqq.com)\n")
        if not self.check_push_url(self.ftqq_url.strip()):
            exit("推送地址有误，请检查！")

        #定义网站更新检查时间间隔，默认值30分钟
        self.check_update_time = 30
        #当前是否首次运行
        self.firstRun = False

    #检查用户输入的推送地址是否有误
    def check_push_url(self, url):
        if not url:
            return False

        post_data = {
            "text": "测试信息",
            "desp": "电影更新推送测试"+str(time.time())
        }
        r = requests.post(url, post_data)
        result_data = r.json()
        if result_data['errno'] == 0:
            print("验证通过!")
            return True
        else:
            return False

    #电影网站获取数据处理
    def movies_deal(self, movies):
        exist_movies = self.getStoredMovies()
        fetched_movies = self.movies_encode(movies)

        #找到新发布的电影
        new_movies = []
        new_movies_str = []
        for i in range(len(fetched_movies)):
            # 判断获取的电影是否存在于已存在的电影列表
            try:
                if exist_movies.index(fetched_movies[i]) > -1:
                    pass
            except:
                new_movies.append(movies[i])
                new_movies_str.append(fetched_movies[i]+"\n") #每个元素后加入回车，为后面写入文件做准备

        #推送和保存更新的电影
        self.push_updated_movies(new_movies)
        self.store_updated_movies(new_movies_str)

    #推送更新的电影
    def push_updated_movies(self, new_movies):
        #如果数组为空，则不推送
        if not len(new_movies):
            return

        title_str = "【更新】"
        desp_str = ""

        if len(new_movies) == 1:
            title_str += new_movies[0]['name']
            desp_str += "[" + new_movies[0]['href'] + "]" + new_movies[0]['name']
        else:
            for movie in new_movies:
                title_str += movie['name'][:5] + '-'
                desp_str += "[" + movie['href'] + "]" + movie['name'] + "-"

        title_str = title_str.strip("-")
        desp_str = desp_str.strip("-")

        #发起请求
        r = requests.post(self.ftqq_url, data={"text": title_str, "desp": desp_str})
        result_data = r.json()

        if result_data['errno'] == 0:
            print("微信消息推送成功！")

    #存储更新的电影到文件
    def store_updated_movies(self, new_movies_str):
        with open("movies.txt", "a+", encoding="utf-8") as fd:
            fd.writelines(new_movies_str)

        return

    #将电影数据进行md5加密，便于存储与比较
    def movies_encode(self, movies):
        movies_arr = []
        for i in range(len(movies)):
            movie_str = movies[i]['name'] + movies[i]['href'] + movies[i]['from']

            hashed_movie = hashlib.md5(movie_str.encode())
            movies_arr.append(hashed_movie.hexdigest())

        return movies_arr

    #获取已经存储的电影数据，用于对比是否有更新
    def getStoredMovies(self):
        movies = []

        if os.path.exists("movies.txt"):
            with open("movies.txt", "r", encoding="utf-8") as fd:
                lines = fd.readlines()

                for line in lines:
                    movies.append(line.strip("\n"))
        else:
            fd = open("movies.txt", "w+", encoding="utf-8")
            fd.close()

        #如果电影数组为空，则认为当次为首次运行
        if not len(movies):
            self.firstRun = True

        return movies

    # 开始按指定时间间隔检查两个网站
    def start(self):
        while True:
            # 初始化两个电影网站对象
            dyttObj = dytt.dytt()
            seehdObj = seehd.seehd()

            # 分别获取两个网站的电影
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(time_now + "开始获取电影更新")

            dytt_movies = dyttObj.getMovies()
            seehd_movies = seehdObj.getMovies()

            # 发送获取到的电影数据
            movies = dytt_movies + seehd_movies
            self.movies_deal(movies)

            # 延时指定时间后再次获取电影数据
            time.sleep(self.check_update_time * 60)

movie_push = movie_push()
movie_push.start()