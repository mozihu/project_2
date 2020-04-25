import requests
from bs4 import BeautifulSoup
import time
import random
import mysqls
import re
from fake_useragent import UserAgent
import os

ua = UserAgent()

# 设置cookies
cookie = "fspop=test; cy=2; cye=beijing; _lxsdk_cuid=171967407a136-0a2cc8c9119d67-153f6555-1fa400-171967407a2c8; _lxsdk=171967407a136-0a2cc8c9119d67-153f6555-1fa400-171967407a2c8; _hc.v=c1a758b6-b189-8a2a-acdf-bd8f44c43b6f.1587367119; t_lxid=17196740888c8-0933e91d92b825-153f6555-1fa400-17196740888c8-tid; s_ViewType=10; _lx_utm=utm_source%3Ddp_pc_index; thirdtoken=ccf94609-9466-49c9-b9d4-e836a17d0ed3; _dp.ac.v=397538aa-6133-4c50-b0cb-027f6f1594ee; dplet=ed25c134f9557cc91df77b2bf089e312; dper=0820b46b0e80a770552ad9d83f9c48cd7e612a840e79c494f199f215aa3198b8ae4216ba70440f714888f6d4fdd64623e64ad5b71ccda2b4d155e7c746c384a5d98b2d383d72fc1e5c4fc2d1cc3bee01a698738f6405b1ac3f479f832e30cc80; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%8D%8E%E4%BB%94_936; ctu=e76be41b64bebfbbbff0ac84c9cf89c899104dad3b40a1363a18a1b109a899a3; uamo=18551664870; _lxsdk_s=171b00298be-49a-797-c74%7C%7C715"

# 修改请求头
headers = {
    'User-Agent': ua.random,
    'Cookie': cookie,
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/shop/112714470/review_all/p6'  # 设置跳转路径
}


def getHTMLText(url, code='utf-8'):
    '''获取html页面'''
    try:
        time.sleep(random.random()*6 + 2)
        r = requests.get(url, timeout=5, headers=headers)
        # 判断r.status_code是否等于200
        # 不需要增加额外的if语句，该语句便于利用try-except进行异常处理
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("产生异常")
        return "产生异常"


def remove_emoji(text):
    '''因为评论中带有emoji表情，是4个字符长度的，mysql数据库不支持4个字符长度，因此要进行过滤'''
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'', text)


def parsePage(html, shpoID):
    '''从html中提起所需字段信息'''
    infoList = []  # 用于存储提取后的信息，列表的每一项都是一个字典
    soup = BeautifulSoup(html, 'html.parser')

    for item in soup('div', 'main-review'):
        comment_content = item.find('div', 'review-words').text.strip()
        infoList.append({'comment_content': remove_emoji(comment_content)})

    return infoList


def getCommentinfo(shop_url, shopID, page_begin, page_end):
    for i in range(page_begin, page_end):
        try:
            url = shop_url + 'p' + str(i)
            html = getHTMLText(url)
            infoList = parsePage(html, shopID)
            print('成功爬取第{}页数据,有评论{}条'.format(i, len(infoList)))
            for info in infoList:
                mysqls.save_data(info)

            # 断点续传中的断点
            if (html != "产生异常") and (len(infoList) != 0):
                with open('xuchuan.txt', 'a') as file:
                    duandian = str(i) + '\n'
                    file.write(duandian)
            else:
                print('休息60s...')
                time.sleep(60)
        except:
            print('跳过本次')
            continue
    return


def xuchuan():
    if os.path.exists('xuchuan.txt'):
        file = open('xuchuan.txt', 'r')
        nowpage = int(file.readlines()[-1])
        file.close()
    else:
        nowpage = 0
    return nowpage


def craw_comment(shopID='112714470', page_end=50):
    '''根据店铺id，店铺页码进行爬取'''
    shop_url = "http://www.dianping.com/shop/" + shopID + "/review_all/"
    nowpage = xuchuan()
    mysqls.create_table()
    getCommentinfo(shop_url, shopID, page_begin=nowpage+1, page_end=page_end)
    mysqls.close_sql()
    return


if __name__ == "__main__":
    craw_comment()
