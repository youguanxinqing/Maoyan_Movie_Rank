"""
配置文件
"""


URL = "http://maoyan.com/board/4?offset=0"


HEADERS = {
    "Host": "maoyan.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/66.0.3359.139 Safari/537.36"
}

# 用于存放请求失败的url
FAILURE = []