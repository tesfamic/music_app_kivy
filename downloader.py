
from urllib.request import urlopen

from pytube import YouTube
from pytube import extract
import json
import random
import os
import time
import requests
# import urllib.request

class MusicDownloader():
    def __init__(self):
        self.music_list = []
        self.saved_music = []
        self.music_titles = dict()
        # self.thumbnail_list = []
        self.number_of_tracks = 0      
        self.load_musiclist()

    def download_audio(self):
        print("Downloading audio.")
        #print("#track:",self.track_counter)
        counter = 0
        for link in self.music_list:
            id = str(extract.video_id(link))
            if id in self.saved_music:
                continue
            yt = YouTube(link)
            # print(yt.streams)
            try:
                # yt = YouTube(link)
                song_obj = yt.streams.get_by_itag(140)                
                stream_success = True
            except:
                stream_success = False
                print("Getting song by Itag obj failed.")
                return 
            if stream_success:
                ## download & save audio
                music_path = 'offline/'+id+'.mp4'
                thmbn_path = 'offline/'+id+'.jpg'
                musicp= song_obj.download(filename=music_path, max_retries=2)              
                ## download & save thumbnail image
                image_data = requests.get(yt.thumbnail_url).content
                with open(thmbn_path,'wb') as handler:
                    handler.write(image_data)  
                print('#{}: {}'.format(counter,yt.title))
                counter += 1
                
            if counter == 500:
                break
            
            # time.sleep(3)

    def load_musiclist(self):
        print("loading playlist")
        url = "https://raw.githubusercontent.com/tesfamic/ceilbot/master/plist.json"        
        try:
            jfile = json.loads(requests.get(url).text)
            # print('online data')
        except:    
            print("Unable to download music list from github.")
            return 
        
        for chnl in jfile:
            #print('Channel:',chnl)
            for vid_id in jfile[chnl]:
                lnk = 'https://www.youtube.com/watch?v=' + str(vid_id)
                self.music_list.append(lnk)
                # self.music_titles[vid_id] = jfile[chnl][vid_id]['title']

        random.shuffle(self.music_list)
        print(" loading completed: ", len(self.music_list))
        # self.number_of_tracks = len(self.music_list)
        files = os.listdir('offline/')
        lists = set()
        for f in files:
            # v_id = f.split('.')[0]
            lists.add(f.split('.')[0])
        self.saved_music = list(lists)
        # self.music_list = list(self.saved_music)
        # self.number_of_tracks = len(self.music_list)        
        print(" #saved music:",len(self.saved_music))


if __name__ == "__main__":
    ethmusic = MusicDownloader()
    ethmusic.download_audio()

    print(" Done. ")
    