from PySide6.QtCore import QObject,Signal
from PySide6.QtMultimedia import QMediaPlayer
from core.database import Database
from core.settings import Settings
from core.player_controller import PlayerController

class FakeAudio:
    def __init__(self): self.v=0
    def setVolume(self,v): self.v=v
class FakePlayer(QObject):
    playbackStateChanged=Signal(object); positionChanged=Signal(int); durationChanged=Signal(int)
    mediaStatusChanged=Signal(object); errorOccurred=Signal(object,int,str)
    def __init__(self): super().__init__(); self.s=QMediaPlayer.StoppedState; self.p=0
    def setAudioOutput(self,a): pass
    def setSource(self,u): self.url=u
    def playbackState(self): return self.s
    def position(self): return self.p
    def duration(self): return 100000
    def setPosition(self,p): self.p=p; self.positionChanged.emit(p)
    def play(self): self.s=QMediaPlayer.PlayingState; self.playbackStateChanged.emit(self.s)
    def pause(self): self.s=QMediaPlayer.PausedState; self.playbackStateChanged.emit(self.s)
    def stop(self): self.s=QMediaPlayer.StoppedState; self.playbackStateChanged.emit(self.s)
    def setPlaybackRate(self,v): self.rate=v

def setup(tmp_path):
    db=Database(tmp_path/"db.sqlite"); settings=Settings(db)
    audio=FakeAudio(); player=FakePlayer()
    ctl=PlayerController(db,settings,player=player,audio=audio)
    paths=[]
    for name in ("one.mp3","two.mp3"):
        p=tmp_path/name; p.write_bytes(b"x")
        paths.append({"id":db.upsert_track({"path":str(p),"title":name}),"path":str(p),"title":name})
    return ctl,player,audio,paths

def test_volume_pause_resume(tmp_path):
    c,p,a,tracks=setup(tmp_path); c.playList(tracks,0)
    c.togglePlay(); c.togglePlay()
    c.setVolume(0); assert a.v==0
    c.setVolume(100); assert a.v==1
    c.shutdown()

def test_skip_last_stops(tmp_path):
    c,p,a,t=setup(tmp_path); c.playList(t,1); c.skip()
    assert p.s==QMediaPlayer.StoppedState
    c.shutdown()

def test_retry_at_start_safe(tmp_path):
    c,p,a,t=setup(tmp_path); c.playList(t,0); p.p=0; c.retry()
    assert c.title
    c.shutdown()

def test_seek_and_switch_track(tmp_path):
    c,p,a,t=setup(tmp_path); c.playList(t,0); c.seek(5000); c.playList(t,1)
    assert c.title=="two.mp3"
    c.shutdown()
