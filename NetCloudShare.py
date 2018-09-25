import json
import random
import urllib.request
import urllib.parse
from selenium import webdriver
import time
base_url = r'http://music.163.com/api/'
music_list_url = r'user/playlist/?offset=0&limit=64&uid=97752165'
list_info_url = r'playlist/detail?id='
commet_url = r'v1/resource/comments/{0}/?rid={1}&\offset=0&total=fasle&limit=100'
qzone_url = r'https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?'
request_map = {
    'site' : '网易云音乐'
}

head =  {
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests' : '1',
    'Cache-Control':'max-age=0'
}
def http_util(url,head):
    res = urllib.request.urlopen(urllib.request.Request(url, None,head)).read().decode('utf-8')
    return res

# 登录
def login_qzone(driver):
    print("##### start get Login Page #####")
    # 切换账号密码登录
    time.sleep(2)
    driver.switch_to.frame('loginFrame')
    driver.find_element_by_id("switcher_plogin").click()
    # 等待Dom 加载
    time.sleep(2)
    driver.find_element_by_id('u').send_keys('------')
    time.sleep(2)
    driver.find_element_by_id('p').send_keys('------')
    time.sleep(4)
    driver.find_element_by_id("login_button").click()
    print("#### Login Success ####")

# 获取‘南宫鸢泽’关联的所有歌单
def user_base_list():
    res =  http_util(base_url + music_list_url,head)
    temp = json.loads(res)
    music_list = {}
    for i in temp['playlist']:
        music_list[i['name']] = (i['id'])
    return music_list
# 随机挑选一个歌单 并选择其中的一首获取热评和歌曲信息
def music_list_hot():
    id = random.choice(list(user_base_list().values()))
    res = http_util(base_url + list_info_url + str(id), head)
    temp = json.loads(res)['result']
    comment_list = {}
    pic_list = {}
    artis_list = {}
    music_name = {}
    if len(temp['tracks']) > 0:
        for i in temp['tracks']:
            comment_list[i['id']] = (i['commentThreadId'])
            pic_list[i['id']] = (i['album']['picUrl'])
            music_name[i['id']] = (i['album']['name'])
            # 暂时只取一个歌手
            artis_list[i['id']] = (i['album']['artists'][0]['name'])
    return comment_list,artis_list,pic_list,music_name
# 随机取一首歌，并加载热评，随机选取一条
def get_end():
    listKL = music_list_hot()
    comment_list = listKL[0]
    pic_list = listKL[2]
    artis_list = listKL[1]
    music_name = listKL[3]
    id = random.choice(list(comment_list.keys()))
    res = http_util(str(base_url + commet_url).format(comment_list[id],comment_list[id]) , head)
    temp = json.loads(res)['hotComments']
    if len(temp) is 0:
        raise RuntimeError('#### 没有热评')
    return random.choice(temp)['content'],id,pic_list[id],artis_list[id],music_name[id]

# --------
def ROOIKE():
    # 获取分享内容
    results = get_end()
    # 组装分享
    if len(results[0]) > 120:
        raise RuntimeError('#### 热评的B话太多了')
    request_map['desc'] = results[0]
    request_map['url'] = "https://music.163.com/song?id=" + str(results[1]) + "&userid=97752165&from=qzone"
    request_map['title'] = "分享单曲：" + results[4]
    request_map['summary'] = results[3]
    request_map['pics'] = results[2] + "?imageView&thumbnail=120y120"
    urls = qzone_url + urllib.parse.urlencode(request_map)

    driver = webdriver.Chrome()
    driver.get(urls)
    # 获取登录session
    driver.find_element_by_id("changeAccounts").click()
    login_qzone(driver)
    # 跳出登录弹窗
    driver.switch_to.default_content()
    print("##### start Push #####")
    time.sleep(5)
    driver.find_element_by_id("postButton").click()
    print("##### Success Push ####")

# 遭遇异常再来一次..
while True:
        try:
            ROOIKE()
            break
        except ValueError:
            print("遭遇了异常和不测，再推一遍")
