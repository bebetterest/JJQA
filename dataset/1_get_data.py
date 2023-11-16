import requests
import json
import re

def postprocess_lyric(lyric):
    re_lyric = re.findall(r'[[0-9]+&#[0-9]+;[0-9]+&#[0-9]+;[0-9]+].*', lyric)
    if re_lyric:  
        lyric = re_lyric[0]
        lyric = lyric.replace("&#32;", " ")
        lyric = lyric.replace("&#40;", "(")
        lyric = lyric.replace("&#41;", ")")
        lyric = lyric.replace("&#45;", "-")
        lyric = lyric.replace("&#10;", "")
        lyric = lyric.replace("&#38;apos&#59;", "'")
        lyric = lyric.replace("&#39;", "'")#added
        lyric = lyric.replace("&#13","")#added
        result = []
        for sentence in re.split(u"[[0-9]+&#[0-9]+;[0-9]+&#[0-9]+;[0-9]+]", lyric):
            if sentence.strip() != "":
                result.append(sentence)
        return "\n".join(result)
    else:
        lyric = lyric.replace("&#32;", " ")
        lyric = lyric.replace("&#40;", "(")
        lyric = lyric.replace("&#41;", ")")
        lyric = lyric.replace("&#45;", "-")
        lyric = lyric.replace("&#10;", "\n")
        lyric = lyric.replace("&#38;apos&#59;", "'")
        lyric = lyric.replace("&#39;", "'")#added
        lyric = lyric.replace("&#13;","")#added
        return lyric



singer_mid="001BLpXF2DyJe2"
#1379
pages=138
num=10
songlist=[]
songdict={}
for page in range(pages):
    begin=num*page
    song_list_url = f"https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{singer_mid}%22%2C%22begin%22%3A{begin}%2C%22num%22%3A{num}%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"
    response = requests.request("get", song_list_url)
    res_list=json.loads(response.text)["singerSongList"]["data"]["songList"]
    for i in res_list:
        tmp=i["songInfo"]
        song_mid=i["songInfo"]["mid"]
        song_id=i["songInfo"]["id"]
        lyric_url=f"https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={song_id}&format=json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Referer": f"https://y.qq.com/n/yqq/song/{song_mid}.html"
        }
        lyric_res = requests.request("get", lyric_url,headers=headers).text
        post_lyric=""
        try:
            lyric=json.loads(lyric_res)["lyric"]
            post_lyric=postprocess_lyric(lyric)
        except:
            post_lyric="none"
            continue #ignore songs without lyrics
        tmp["lyric"]=post_lyric
        tmp["url"]=f"https://y.qq.com/n/yqq/song/{song_mid}.html"
        tmp["lyric_len"]=len(tmp["lyric"])
        songdict[song_id]=tmp
        songlist.append(tmp)
    print(page)


#save data in a json file
with open("song_info.json","w",encoding='utf-8') as fout:
    json.dump(songdict, fout, indent = 2, ensure_ascii=False) 
print(len(songdict.keys()))
