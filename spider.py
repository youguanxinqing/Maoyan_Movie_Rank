import re
import json
import requests
from CONFIG import *


def get_one_html(url, tries=3):
    """
    获取传递进来的url指向的页面
    :param url:
    :param tries:
    :return:
    """
    try:
        response = requests.get(url=url, headers=HEADERS)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:

        # 如果失败三次，将失败的url加入到FAILURE队列中
        if tries<=0:
            FAILURE.append(url)
            return None

        # 如果该url还未失败三次，重复请求
        else:
            get_one_html(url, tries-1)

    # 请求成功则返回页面内容
    else:
        return response.text


def parse_html(html):
    """
    提取页面中的数据
    包括：排名，封面图片链接，电影名，演员，上映时间，评分
    并且返回字典类型
    :param html:
    :return:
    """
    # 构建合适的正则规则
    pattern = re.compile(
              r'<dd>.*?<i.*?>(\d+?)</i>.*?data-src="(.*?)".*?title="(.*?)".*?'
              r'class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?class'
              r'="integer">(.*?)</i>.*?class="fraction">(.*?)</i>', re.S)
    results = re.findall(pattern, html)

    # 构建字典
    for result in results:
        yield {
            "rank": result[0],
            "img": result[1],
            "name": result[2],
            "actor": result[3].replace(r"\n", "").strip(),
            "time": result[4],
            "score": result[5]+result[6]
        }



def main():
    f = open("Movie_Rank", "w", encoding="utf-8")

    # 构建请求的url地址
    pattern = re.compile(r"\d+$")
    for offset in range(0, 100, 10):
        url = re.sub(pattern, str(offset), URL)
        # print(url)

        html = get_one_html(url)
        if not html:
            continue

        # print(html)
        for item in parse_html(html):
            print(item)
            f.write(json.dumps(item, ensure_ascii=False))
            f.write("\n")

    # 打印失败队列，确认是否存在失败链接
    print(FAILURE)

if __name__ == "__main__":
    main()