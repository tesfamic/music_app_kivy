
from urllib.request import urlopen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from pytube import YouTube
from pytube import extract
import json
import random
import os
import time
import requests
import urllib.request
# import time

class MusicPlayer():
    def __init__(self):
        self.music_list = []
        self.saved_music = []
        self.music_titles = dict()
        # self.thumbnail_list = []
        self.number_of_tracks = 0
        self.track_counter = 0
        self.thumbnail_url = ""
        self.song_title = ""
        self.music_length = 0.0
        self.current_music_path = ""
        self.shuffle_play = 1 #on
        self.sound = None
        self.play_started = False
        self.play_ended = False
        self.playing_pos = 0.0
        self.player_paused = False
        self.end_of_list = False
        self.manual_next = False
        ######
        self.load_playlist()
        self.load_music_titles()
        # self.music_ethnic = False
        if self.number_of_tracks>0:
            self.play()

    def play(self):
        if self.player_paused:
            self.sound.play()
            self.sound.seek(self.playing_pos)
            self.player_paused = False
        else:
            self.play_music()

    def pause(self):
        self.playing_pos = self.sound.get_pos()
        self.player_paused = True
        self.sound.stop()

    def next(self):
        if self.sound:            
            if self.track_counter<len(self.music_list)-1:
                self.track_counter += 1                
            else:
                self.end_of_list = True
                print("End of list.")
                # self.track_counter = 0
            self.sound.stop()
        else:
            self.play_music()

    def previous(self):
        if self.sound:
            if self.track_counter>0:
                self.track_counter -= 1
            else:
                self.track_counter = len(self.music_list)-1
            
            self.sound.stop()
        else:
            self.play_music()

    def play_next(self):
        if self.track_counter<len(self.music_list)-1:
            self.track_counter += 1
            self.play_music()
    
    def shuffle(self):
        if len(self.music_list)>0:
            if self.shuffle_play:
                random.shuffle(self.music_list)

    def restart(self):
        if self.sound:
            self.track_counter = 0
            self.end_of_list = False
            self.sound.stop()
        else:
            self.play_music()

    def play_music(self):
        if self.load_audio():
            self.sound = SoundLoader.load(self.current_music_path)
            self.sound.bind(on_play=self.player_playing,on_stop=self.player_stopped)
            if self.sound:
                self.music_length = self.sound.length
                self.sound.play()
        else:
            print("attempting next...")
            # time.sleep(5)
            if self.track_counter==0:
                self.track_counter += 1
            self.next()
    #########################    
    def player_playing(self, obj):
        self.play_started = True
        self.play_ended = False
        self.manual_next = False

    def player_stopped(self, obj):
        self.play_ended = True
        self.play_started = False

    def load_audio(self):
        print(" Track: {}".format(self.track_counter))
        video_id = self.music_list[self.track_counter]
        # video_id = str(extract.video_id(link))
        path = "T:\eth_muzika\offline"
        f_name = os.path.join(path,video_id+".mp4")
        img_name = os.path.join(path,video_id+".jpg")

        skip_list = ['oromo','ii','uu','aa','ee','oromiyaa','oroomiyaa','jj']

        if video_id in self.music_list:
            self.current_music_path = f_name
            if os.path.exists(img_name):
                self.thumbnail_url = img_name
            else:
                self.thumbnail_url = "default_.png"
            s_title = YouTube("https://www.youtube.com/watch?v=" + str(video_id)).title
            self.song_title = self.music_titles.get(video_id,s_title)
            ### I'm just skipping some of the music tracks ...
            for term in skip_list:
                if term in self.song_title.lower():
                    print(self.song_title)
                    return False
            return True
        return False

    def load_playlist(self):
        #### Downloaded music files are in local disk
        path = "T:\eth_muzika\offline"
        files = os.listdir(path)
        lists = set()
        for f in files:
            # v_id = f.split('.')[0]
            lists.add(f.split('.')[0])
        self.saved_music = list(lists)
        self.music_list = list(self.saved_music)
        self.number_of_tracks = len(self.music_list)        
        # print("#saved music:",len(self.saved_music))

    def load_music_titles(self):
        file = open('music_titles.json','r')
        jfile = json.load(file) 
        for id in jfile:
            self.music_titles[id] = jfile[id]
        # print("#titles:",len(self.music_titles))
        file.close()
