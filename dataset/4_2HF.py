import os, json

tmp_collect_song_dict=None
with open("q_a_song_dic.json","r",encoding='utf-8') as fin:
    tmp_collect_song_dict=json.load(fin)

tmp_q_a_dic=None
if os.path.exists("q_a_dic.json"):
    with open("q_a_dic.json","r",encoding='utf-8') as fin:
        tmp_q_a_dic=json.load(fin)

hg_q_a={"data":[]}

q_a_dic_keys=list(tmp_q_a_dic.keys())
print(len(q_a_dic_keys))
for song_key in q_a_dic_keys:
    for q_a_key in tmp_q_a_dic[song_key].keys():
        tmp=tmp_q_a_dic[song_key][q_a_key]
        tmp["song_id"]=song_key
        tmp["song_title"]=tmp_collect_song_dict[song_key]["title"]
        tmp["id"]=song_key+"_"+q_a_key
        hg_q_a["data"].append(tmp)

with open("hf_q_a.json","w",encoding='utf-8') as fout:
    json.dump(hg_q_a,fout,ensure_ascii=False,indent=2)

hg_song={"data":[]}
for song_key in q_a_dic_keys:
    hg_song["data"].append({
        "id":song_key,
        "title":tmp_collect_song_dict[song_key]["title"],
        "name":tmp_collect_song_dict[song_key]["name"],
        "lyric":tmp_collect_song_dict[song_key]["lyric"],
        "id":song_key
    })
with open("hf_song.json","w",encoding='utf-8') as fout:
    json.dump(hg_song,fout,ensure_ascii=False,indent=2)

song_indx={"data":[{hg_song["data"][ind]["id"]:ind for ind in range(len(hg_song["data"]))}]}
with open("hf_song_indx.json","w",encoding='utf-8') as fout:
    json.dump(song_indx,fout,ensure_ascii=False,indent=2)


import datasets
q_a_dataset=datasets.load_dataset('json', data_files='hf_q_a.json',field="data")["train"]
song_dataset=datasets.load_dataset("json",data_files="hf_song.json",field="data")["train"]
song_ind=datasets.load_dataset("json",data_files="hf_song_indx.json",field="data")["train"]

JJQA_dataset=datasets.DatasetDict({
    "qa":q_a_dataset,
    "song":song_dataset,
    "song_index": song_ind,
})

JJQA_dataset.save_to_disk("JJQA_dataset")