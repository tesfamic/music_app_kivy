
# from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import NumericProperty, StringProperty
# from kivymd.uix.button import MDIconButton,MDTextButton
# from kivy.lang import Builder

# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.image import Image,AsyncImage
from kivy.clock import Clock
from musicplayer import MusicPlayer
from kivy.core.window import Window

Window.size = (450, 600)

class MainUI(MDBoxLayout):

    manual_next = False
    play_state = 0

    icon_type = StringProperty("play-outline")
    shuffle_icon = StringProperty("shuffle")
    thumbnail_url = StringProperty("default_1.png")
    song_title = StringProperty("-- Music Title --")
    song_pos = StringProperty("\n 0.0")
    num_of_tracks = StringProperty("\n #Tracks: 0")
    slider_value = NumericProperty(0.0)
    volume_value = NumericProperty(50)
    volume_icon = StringProperty("volume-medium")
    mplayer = MusicPlayer()

    def __init__(self,**kwargs):
        super(MainUI,self).__init__(**kwargs)
        # self.mplayer = MusicPlayer()
        self.play_event = Clock.schedule_interval(self.player_state_callback, 1 / 2.)
        
    def play_click(self):
        # print("Play button clicked.")
        if self.play_state:
            self.icon_type = "play-outline"
            self.play_state = 0
            self.mplayer.pause()
        else:
            self.icon_type = "pause"
            self.play_state = 1
            self.song_title = " Loading music ...."
            self.mplayer.play()
        # self.update_ui()

    def next_click(self):
        self.mplayer.manual_next = True
        self.mplayer.next()
        # self.update_ui()  

    def previous_click(self):
        self.mplayer.manual_next = True
        self.mplayer.previous()
        # self.update_ui()

    def restart_click(self):
        self.mplayer.restart()
        # self.update_ui()

    def shuffle_click(self):
        if self.mplayer.shuffle_play:
            self.mplayer.shuffle_play = 0 #off
            self.shuffle_icon = "shuffle"
        else:
            self.mplayer.shuffle_play = 1 #on
            self.shuffle_icon = "shuffle-disabled"
        self.mplayer.shuffle()
        # print('shuffle clicked.')

    def update_ui(self):
        self.thumbnail_url = self.mplayer.thumbnail_url
        self.song_title = self.mplayer.song_title
        self.num_of_tracks = "\n #Tracks: "+str(self.mplayer.number_of_tracks)
        # self.song_pos = str(self.mplayer.music_length)
        
    def player_state_callback(self,obj):
        if self.mplayer.play_started:
            self.update_ui()
            pos = self.mplayer.sound.get_pos()
            self.slider_value = 100.0*pos/self.mplayer.music_length
            minute = int(pos/60)
            second = int(pos-minute*60)
            if second<10:
                second = '0'+str(second)
            
            t_min = int(self.mplayer.music_length/60)
            t_sec = int(self.mplayer.music_length-t_min*60)
            if t_sec<10:
                t_sec ='0'+str(t_sec)
            t_time = str(t_min)+':'+str(t_sec)
            self.song_pos = '\n'+str(minute)+':'+str(second)+"/"+t_time
            self.play_state = 1
            self.icon_type = "pause"

        elif self.mplayer.play_ended:
            if self.mplayer.player_paused:
                pass
            else:
                if not self.mplayer.end_of_list:
                    if self.mplayer.manual_next:
                        self.mplayer.play()
                        # self.manual_next = False
                    else:
                        self.mplayer.play_next()

                    self.update_ui()
                    # self.thumbnail_url = self.mplayer.thumbnail_url
                    # self.song_title = self.mplayer.song_title
                else:
                    self.play_state = 0
                    self.mplayer.track_counter = 0
                    self.icon_type = "play-outline" 
                
    def slider_value_change(self,widget):
        self.slider_value = widget.value


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MainUI()

    def on_pause(self):
        return True

if __name__ == "__main__":
    MainApp().run()
