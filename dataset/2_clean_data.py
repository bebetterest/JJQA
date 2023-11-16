
#clean data. clean songs without lyric and those of various versions

import requests
import json
import re

#load json
songdict=None
with open("song_info.json","r",encoding='utf-8') as fin:
    songdict=json.load(fin) 
print("before cleaning:",len(songdict.keys()))


#data cleaning
key_list=list(songdict.keys())
total_length=len(key_list)
collect_song_list=[]
collect_song_key_dict={}
collect_song_dict={}

plus_del_num=0
pure_del_num=0
min_del_num=0

for key in key_list:
    song=songdict[key]
    if("+" in song["name"]):
        plus_del_num=plus_del_num+1
        del songdict[key]
    elif("纯音乐" in song["lyric"]):
        pure_del_num=pure_del_num+1
        del songdict[key]
    # elif("请您欣赏" in song["lyric"]):
    #     pure_del_num=pure_del_num+1
    #     del songdict[key]
    # elif(len(song["lyric"])<=50):
    #     pure_del_num=pure_del_num+1
    #     del songdict[key]
    else:
        if(song["name"]==song["title"]):
            # try:
            #     assert (song["name"] in collect_song_list)==0
            # except:
            #     print(song["name"])
            #     continue
            collect_song_list.append(song["name"].strip())
            collect_song_key_dict[song["name"]]=key
            collect_song_dict[key]=song
            del songdict[key]

print("deleted:",plus_del_num+pure_del_num)
print("collect_num after step1:",len(list(collect_song_dict.keys())))
assert total_length==(plus_del_num+pure_del_num+len(list(collect_song_dict.keys()))+len(list(songdict.keys())))


key_list=list(songdict.keys())

for key in key_list:
    song=songdict[key]
    if((song["name"].strip() in collect_song_list)==False):
        collect_song_list.append(song["name"])
        collect_song_key_dict[song["name"]]=key
        collect_song_dict[key]=song
        del songdict[key]
        
print("collect_num after step2:",len(list(collect_song_dict.keys())))
assert total_length==(plus_del_num+pure_del_num+len(list(collect_song_dict.keys()))+len(list(songdict.keys())))
print("left:",len(songdict.values()))


#save cleaned data
with open("cleaned_song_info.json","w",encoding='utf-8') as fin:
    json.dump(collect_song_dict,fin,indent = 2, ensure_ascii=False)