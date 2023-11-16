#coding = 'utf-8'

import sys
import json
import numpy as np
import pinyin
import os
from selenium import webdriver
from selenium.webdriver import Firefox
from PyQt5 import QtCore, QtWidgets
from Ui_label import Ui_Dialog

class LUI(Ui_Dialog):
    def __init__(self):
        super().__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.collect_song_dict={}
        self.q_a_dic={}

        self.first_load=True

        self.q_a_song_key=None
        self.q_a_index=None

        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.page_load_strategy = 'none'
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")


        self.driver1=Firefox(executable_path="geckodriver.exe",options=options)
        self.driver2=Firefox(executable_path="geckodriver.exe",options=options)

        tmp_collect_song_dict=None
        if os.path.exists("q_a_song_dic.json"):
            with open("q_a_song_dic.json","r",encoding='utf-8') as fin:
                tmp_collect_song_dict=json.load(fin)
        else:
            with open("cleaned_song_info.json","r",encoding='utf-8') as fin:
                tmp_collect_song_dict=json.load(fin)
        
        print(len(tmp_collect_song_dict.keys()))

        tmp_q_a_dic=None
        if os.path.exists("q_a_dic.json"):
            with open("q_a_dic.json","r",encoding='utf-8') as fin:
                tmp_q_a_dic=json.load(fin)
        print(len(tmp_q_a_dic.keys()))

        ##sort by lyric length
        # tmp_keys=list(tmp_collect_song_dict.keys())
        # lens=[len(tmp_collect_song_dict[key]["lyric"]) for key in tmp_keys]
        # sorted_indx=np.argsort(lens)
        # for ind in sorted_indx:
        #     key=tmp_keys[ind]
        #     self.collect_song_dict[key]=tmp_collect_song_dict[key]
        #     if key in tmp_q_a_dic.keys():
        #         self.q_a_dic[key]=tmp_q_a_dic[key]

        #sort by title pinyin
        tmp_list=list(tmp_collect_song_dict.values())
        tmp_list.sort(key=lambda x:pinyin.get(x["title"], format="strip", delimiter=""))
        for item in tmp_list:
            self.collect_song_dict[item["id"]]=item
            if str(item["id"]) in tmp_q_a_dic.keys():
                self.q_a_dic[str(item["id"])]=tmp_q_a_dic[str(item["id"])]




    def bind_func(self):
        self.playing_song=None
        # self.timer=QtCore.QTimer()
        # self.timer.timeout.connect(self.timer_driver_fun)
        self.play_song.clicked.connect(self.driver_fun)
    
        self.song_list.currentRowChanged.connect(self.song_change_fun)

        self.qa_list.currentRowChanged.connect(self.show_qa_fun)

        self.add_qa.clicked.connect(self.add_qa_fun)
        self.delete_qa.clicked.connect(self.delete_qa_fun)

        self.previous_song.clicked.connect(self.previous_song_fun)
        self.next_song.clicked.connect(self.next_song_fun)

        self.delete_song.clicked.connect(self.delete_song_fun)

        self.lyric_list.itemSelectionChanged.connect(self.rf_update)

        self.q_text.textChanged.connect(self.q_change_for_qalist_fun)
    
    def q_change_for_qalist_fun(self):
        if(self.q_a_index==None or self.q_a_index==-1):
            return
        new_text=self.q_text.toPlainText().strip()
        item=self.qa_list.item(self.q_a_index)
        item.setText( self._translate("Dialog", str(self.q_a_index)+". "+new_text))

    def song_change_fun(self):
        if(self.first_load):
            pass
        else:
            if(self.save_qa_online()):
                self.save_offline()
        self.show_lyric_and_info_fun()
        self.show_qa_list_fun()
    
    def rf_update(self):
        current_row=self.lyric_list.currentRow()
        if(current_row==-1):
            return
        selected_list=self.lyric_list.selectedIndexes()
        selected_rows=[_.row() for _ in selected_list]

        if(current_row in selected_rows ):#select lines with the same lyric
            cuttent_song=self.collect_song_dict[list(self.collect_song_dict.keys())[self.song_list.currentRow()]]
            song_lyrics=cuttent_song["lyric"].strip().split("\n")
            selected_lyric=song_lyrics[current_row].strip()

            for line in range(len(song_lyrics)):
                if((line==current_row) or (line in selected_rows)):
                    continue
                if(song_lyrics[line].strip()==selected_lyric):
                    self.lyric_list.item(line).setSelected(True)
        # else:
        #     cuttent_song=self.collect_song_dict[list(self.collect_song_dict.keys())[self.song_list.currentRow()]]
        #     song_lyrics=cuttent_song["lyric"].strip().split("\n")
        #     selected_lyric=song_lyrics[current_row].strip()

        #     for line in range(len(song_lyrics)):
        #         if((line==current_row) or (line not in selected_rows)):
        #             continue
        #         if(song_lyrics[line].strip()==selected_lyric):
        #             self.lyric_list.item(line).setSelected(False) 


        selected_list=self.lyric_list.selectedIndexes()
        indexes=[]
        for selected in selected_list:
            indexes.append(selected.row()) 
        indexes=sorted(indexes)

        rf_text=""
        for index in indexes:
            rf_text=rf_text+str(index)+" "
        rf_text=rf_text.strip()
        self.rf_browser.setHtml(rf_text)        

    # def timer_driver_fun(self):
    #     index=self.song_list.currentRow()
    #     if(index==-1):
    #         return
    #     now_song_key=list(self.collect_song_dict.keys())[index]
    #     if(self.playing_song==now_song_key):
    #         return
    #     self.playing_song=now_song_key

    #     song=self.collect_song_dict[now_song_key]
    #     self.driver1.get(song["url"])
    #     self.driver2.get("https://www.baidu.com/s?wd=歌曲 "+song["name"])
    #     try:
    #         self.driver1.find_element_by_class_name("mod_btn_green").click()# try to play the song in QQMusic
    #     except:
    #         pass
    #         # QtWidgets.QMessageBox.about(None,"warning","something wrong when trying to play the music")
        
    def driver_fun(self):
        index=self.song_list.currentRow()
        if(index==-1):
            return
        now_song_key=list(self.collect_song_dict.keys())[index]
        if(self.playing_song==now_song_key):
            return
        self.playing_song=now_song_key

        song=self.collect_song_dict[now_song_key]
        self.driver1.get(song["url"])
        self.driver2.get("https://www.baidu.com/s?wd=歌曲 "+song["name"])
        try:
            self.driver1.find_element_by_class_name("mod_btn_green").click()# try to play the song in QQMusic
        except:
            pass
            # QtWidgets.QMessageBox.about(None,"warning","something wrong when trying to play the music")

    def delete_song_fun(self):
        index=self.song_list.currentRow()
        if(index==-1):
            return
        
        song=self.collect_song_dict[list(self.collect_song_dict.keys())[index]]
        del self.collect_song_dict[list(self.collect_song_dict.keys())[index]]
        if(str(song["id"]) in list(self.q_a_dic.keys())):
            del self.q_a_dic[str(song["id"])]

        self.save_offline()
        
        self.song_list.clear()
        self.load_song_list_fun()
        if(index!=0):
            index=index-1
        if(len(self.collect_song_dict.keys())==0):
            index=-1
        self.song_list.setCurrentRow(index)


    def previous_song_fun(self):
        if(self.save_qa_online()):
            self.save_offline()
        self.song_list.setCurrentRow(self.song_list.currentRow()-1)
        if(self.song_list.currentRow()==-1):
            self.song_list.setCurrentRow(len(self.collect_song_dict.keys())-1)
        

    def next_song_fun(self):
        if(self.save_qa_online()):
            self.save_offline()
        self.song_list.setCurrentRow(self.song_list.currentRow()+1)
        if(self.song_list.currentRow()==-1):
            if(len(self.collect_song_dict.keys())==0):
                self.song_list.setCurrentRow(-1)
            else:
                self.song_list.setCurrentRow(0)
        

    def load_song_list_fun(self):
        self.song_list.clear()
        if(len(list(self.collect_song_dict.keys()))==0):
            self.song_list.setCurrentRow(-1)
            return
        for index in range(len(list(self.collect_song_dict.keys()))):
            key=list(self.collect_song_dict.keys())[index]
            song=self.collect_song_dict[key]
            
            item=QtWidgets.QListWidgetItem()
            item.setText( self._translate("Dialog", "%03d: "%index+song["title"]))
            self.song_list.addItem(item)
        self.song_list.setCurrentRow(0)
        # self.timer.start(1000*3)
        
    
    def show_lyric_and_info_fun(self):
        self.lyric_list.clear()
        index=self.song_list.currentRow()
        if(index==-1):
            return
        song=self.collect_song_dict[list(self.collect_song_dict.keys())[index]]
        
        lyric=song["lyric"].strip().split("\n")
        self.lyric_list.clear()
        for line in range(len(lyric)):
            lyric[line]=lyric[line].strip()
            item=QtWidgets.QListWidgetItem()
            item.setText( self._translate("Dialog", "%03d: "%line+lyric[line]))
            self.lyric_list.addItem(item)
        self.lyric_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)#key

        tmp_idx=index
        tmp_sum=len(self.collect_song_dict.keys())
        tmp_name=song["name"]
        tmp_title=song["title"]
        tmp_id=song["id"]
        s_info_text="index: \n%d/%d\nname: \n%s\ntitle: \n%s\nid: \n%d"%(tmp_idx,tmp_sum,tmp_name,tmp_title,tmp_id)
        self.info_text.setPlainText(s_info_text)

    def show_qa_list_fun(self):
        self.qa_list.clear()
        index=self.song_list.currentRow()
        if(index==-1):
            self.qa_list.setCurrentRow(-1)
            return
        song=self.collect_song_dict[list(self.collect_song_dict.keys())[index]]

        self.qa_list.clear()
        if str(song["id"]) in list(self.q_a_dic.keys()):
            q_as=self.q_a_dic[str(song["id"])]
            for key in q_as.keys():
                q_a=q_as[key]
                item=QtWidgets.QListWidgetItem()
                item.setText( self._translate("Dialog", key+". "+q_a["q"]))
                self.qa_list.addItem(item)
            self.qa_list.setCurrentRow(0)

    def show_qa_fun(self):
        if(self.first_load):
            self.first_load=False
        else:
            if(self.save_qa_online()):
                self.save_offline()

        self.a_text.clear()
        self.q_text.clear()
        self.rf_browser.clear()
        self.lyric_list.clearSelection()
        
        if(self.qa_list.currentRow()==-1):
            self.q_text.clear()
            self.a_text.clear()
            self.rf_browser.clear()
            self.q_a_song_key=None
            self.q_a_index=None
            return
        index=self.qa_list.currentRow()
        song_key=list(self.collect_song_dict.keys())[self.song_list.currentRow()]
        song=self.collect_song_dict[song_key]
        q_as=self.q_a_dic[str(song["id"])]
        q_a=q_as[list(q_as.keys())[index]]
        self.q_text.setPlainText(q_a["q"])
        self.a_text.setPlainText(q_a["a"])

        rf=q_a["rf"].strip()
        self.rf_browser.setHtml(rf)
        rf_list=None
        if(rf==""):
            rf_list=[]
        else:
            rf_list=rf.split(" ")
            rf_list=[int(_.strip()) for _ in rf_list]
        
        for index in rf_list:
            self.lyric_list.item(index).setSelected(True)

        self.q_a_song_key=song_key
        self.q_a_index=self.qa_list.currentRow()
    
    def add_qa_fun(self):
        if(self.save_qa_online()):
            self.save_offline()
        song_index=self.song_list.currentRow()
        song_key=list(self.collect_song_dict.keys())[song_index]
        song=self.collect_song_dict[song_key]
        if(str(song["id"]) not in list(self.q_a_dic.keys())):
            self.q_a_dic[str(song["id"])]={}
        self.q_a_dic[str(song["id"])][str(len(self.q_a_dic[str(song["id"])]))]={"q":"question here","a":"answer here","rf":""}
        self.show_qa_list_fun()
        self.qa_list.setCurrentRow(len(self.q_a_dic[str(song["id"])])-1)


    def delete_qa_fun(self):
        song_index=self.song_list.currentRow()
        song_key=list(self.collect_song_dict.keys())[song_index]
        song=self.collect_song_dict[song_key]

        tmp_qa_row=self.qa_list.currentRow()
        if(tmp_qa_row==-1):
            return
        
        del self.q_a_dic[str(song["id"])][str(tmp_qa_row)]
        self.q_a_index=None
        self.q_a_song_key=None

        totle_len=len(self.q_a_dic[str(song["id"])])
        new_qas={}
        for i in range(totle_len):
            new_qas[str(i)]=self.q_a_dic[str(song["id"])][list(self.q_a_dic[str(song["id"])].keys())[i]]
        self.q_a_dic[str(song["id"])]=new_qas

        self.save_offline()

        self.show_qa_list_fun()
        if(tmp_qa_row==0):
            if(len(new_qas.keys())==0):
                self.qa_list.setCurrentRow(-1)
            else:
                self.qa_list.setCurrentRow(0)
        else:
            self.qa_list.setCurrentRow(tmp_qa_row-1)


    def save_qa_online(self):

        song_key=self.q_a_song_key
        if((song_key in list(self.collect_song_dict.keys()))==False):
            return False
        song=self.collect_song_dict[song_key]

        qa_index=self.q_a_index

        if((str(qa_index) in list(self.q_a_dic[str(song["id"])].keys()))==False):
            return False

        tmp_q=self.q_text.toPlainText().strip()
        tmp_a=self.a_text.toPlainText().strip()
        tmp_rf=self.rf_browser.toPlainText().strip()
        
        if(tmp_q=="" or tmp_a=="" or tmp_rf==""):
            QtWidgets.QMessageBox.about(None,"warning","q/a/rf is empty!")
        
        self.q_a_dic[str(song["id"])][str(qa_index)]["q"]=tmp_q
        self.q_a_dic[str(song["id"])][str(qa_index)]["a"]=tmp_a
        self.q_a_dic[str(song["id"])][str(qa_index)]["rf"]=tmp_rf

        self.q_a_song_key=None
        self.q_a_index=None

        return True

    def save_offline(self):
        with open("q_a_song_dic.json","w",encoding='utf-8') as fout:
            json.dump(self.collect_song_dict,fout,indent = 2, ensure_ascii=False)
        with open("q_a_dic.json","w",encoding='utf-8') as fout:
            json.dump(self.q_a_dic,fout,indent = 2, ensure_ascii=False)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = LUI()
ui.setupUi(MainWindow)
MainWindow.show()
ui.bind_func()

ui.load_song_list_fun()

sys.exit(app.exec_())