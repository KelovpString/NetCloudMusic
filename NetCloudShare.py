import json
import random
import urllib.request

base_url = r'http://music.163.com/api/'
music_list_url = r'user/playlist/?offset=0&limit=64&uid=97752165'
list_info_url = r'playlist/detail?id='
commet_url = r'v1/resource/comments/{0}/?rid={1}&\offset=0&total=fasle&limit=100'
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
    if len(temp['tracks']) > 0:
        for i in temp['tracks']:
            comment_list[i['id']] = (i['commentThreadId'])
    return comment_list
# 随机取一首歌，并加载热评，随机选取一条
def get_end():
    comment_list = music_list_hot()
    id = random.choice(list(comment_list.keys()))
    res = http_util(str(base_url + commet_url).format(comment_list[id],comment_list[id]) , head)
    temp = json.loads(res)['hotComments']
    return random.choice(temp)['content'],id
print(get_end())



