from pathlib import Path
import random,time
from PySide6.QtCore import QObject,Signal,Slot,Property,QUrl
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
class PlayerController(QObject):
    stateChanged=Signal(); trackChanged=Signal(); positionChanged=Signal(); durationChanged=Signal()
    volumeChanged=Signal(); shuffleChanged=Signal(); repeatChanged=Signal(); toast=Signal(str); queueChanged=Signal()
    def __init__(self,db,settings,parent=None,player=None,audio=None):
        super().__init__(parent); self.db=db; self.settings=settings
        self.audio=audio or QAudioOutput(self); self.player=player or QMediaPlayer(self)
        self.player.setAudioOutput(self.audio)
        self._queue=[]; self._index=-1; self._track=None; self._history=[]
        self._shuffle=bool(settings.get("shuffle",False)); self._repeat=str(settings.get("repeat","off"))
        self._volume=max(0,min(100,int(settings.get("volume","70")))); self._last_volume=self._volume or 70
        self.audio.setVolume(self._volume/100); self._last_action=0
        self.player.playbackStateChanged.connect(self.stateChanged.emit)
        self.player.positionChanged.connect(self.positionChanged.emit)
        self.player.durationChanged.connect(self.durationChanged.emit)
        self.player.mediaStatusChanged.connect(self._status); self.player.errorOccurred.connect(self._error)
    @Property(str,notify=stateChanged)
    def state(self):
        s=self.player.playbackState()
        return "playing" if s==QMediaPlayer.PlayingState else "paused" if s==QMediaPlayer.PausedState else "stopped"
    @Property(str,notify=trackChanged)
    def title(self): return self._track.get("title","") if self._track else "Nada tocando"
    @Property(str,notify=trackChanged)
    def artist(self): return self._track.get("artist","") if self._track else "Escolha uma música"
    @Property(int,notify=volumeChanged)
    def volume(self): return self._volume
    @Property(bool,notify=shuffleChanged)
    def shuffle(self): return self._shuffle
    @Property(str,notify=repeatChanged)
    def repeat(self): return self._repeat
    @Property(int,notify=positionChanged)
    def position(self): return self.player.position()
    @Property(int,notify=durationChanged)
    def duration(self): return self.player.duration()
    @Property("QVariantList",notify=queueChanged)
    def queue(self): return self._queue
    def _play_index(self,i):
        if not 0<=i<len(self._queue): return
        t=self._queue[i]
        if not Path(t["path"]).is_file():
            self.toast.emit("Arquivo não encontrado; pulando para a próxima faixa.")
            self._advance_bad(i); return
        if self._track and self._track.get("path")!=t.get("path"): self._history.append(self._track)
        self._index=i; self._track=t
        self.player.setSource(QUrl.fromLocalFile(str(Path(t["path"]).resolve())))
        self.db.record_play(t); self.trackChanged.emit(); self.queueChanged.emit(); self.player.play()
    @Slot("QVariantList",int)
    def playList(self,tracks,index=0):
        self._queue=[dict(t) for t in tracks]; self._index=-1; self.queueChanged.emit()
        if self._queue: self._play_index(max(0,min(index,len(self._queue)-1)))
    @Slot("QVariantMap")
    def playTrack(self,t): self._queue=[dict(t)]; self._index=-1; self._play_index(0)
    @Slot()
    def togglePlay(self):
        if self.player.playbackState()==QMediaPlayer.PlayingState: self.player.pause()
        elif self._track: self.player.play()
        elif self._queue: self._play_index(0)
    @Slot()
    def skip(self):
        if time.monotonic()-self._last_action<.08: return
        self._last_action=time.monotonic()
        if self._repeat=="one": self.player.setPosition(0); self.player.play(); return
        n=self._next()
        if n is None: self.player.stop(); self.player.setPosition(0); self.toast.emit("Fim da fila."); return
        self._play_index(n)
    def _next(self):
        if not self._queue: return None
        if self._shuffle and len(self._queue)>1: return random.choice([i for i in range(len(self._queue)) if i!=self._index])
        n=self._index+1
        if n<len(self._queue): return n
        return 0 if self._repeat=="all" else None
    @Slot()
    def previous(self):
        if self._history:
            t=self._history.pop()
            if t in self._queue: self._play_index(self._queue.index(t))
            else: self._queue.insert(0,t); self._play_index(0)
        elif self._index>0: self._play_index(self._index-1)
        elif self._queue: self._play_index(0)
    @Slot()
    def retry(self):
        if self.player.position()>3000: self.player.setPosition(0)
        else: self.previous()
    @Slot()
    def toggleShuffle(self): self._shuffle=not self._shuffle; self.settings.set("shuffle",self._shuffle); self.shuffleChanged.emit()
    @Slot()
    def cycleRepeat(self):
        self._repeat={"off":"all","all":"one","one":"off"}[self._repeat]; self.settings.set("repeat",self._repeat); self.repeatChanged.emit()
    @Slot(int)
    def setVolume(self,v):
        self._volume=max(0,min(100,int(v)))
        if self._volume: self._last_volume=self._volume
        self.audio.setVolume(self._volume/100); self.settings.set("volume",self._volume); self.volumeChanged.emit()
    @Slot()
    def toggleMute(self): self.setVolume(0 if self._volume else self._last_volume)
    @Slot(int)
    def seek(self,v): self.player.setPosition(max(0,min(int(v),self.player.duration())))
    @Slot(int)
    def seekRelative(self,v): self.seek(self.player.position()+v)
    def _status(self,status):
        if status==QMediaPlayer.EndOfMedia: self.skip()
        elif status==QMediaPlayer.InvalidMedia: self._bad("Mídia inválida ou codec não suportado.")
    def _error(self,*args): self._bad(str(args[-1]) if args else "Erro de reprodução.")
    def _bad(self,msg):
        self.toast.emit(msg)
        if self._index>=0: self._advance_bad(self._index)
    def _advance_bad(self,i):
        if i+1<len(self._queue): self._play_index(i+1)
        elif self._repeat=="all" and self._queue: self._play_index(0)
        else: self.player.stop()
    def shutdown(self):
        self.settings.set("last_track",self._track.get("path","") if self._track else "")
        self.settings.set("last_position",self.player.position()); self.player.stop()
