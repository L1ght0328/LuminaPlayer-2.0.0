from PySide6.QtCore import QObject,Signal,Slot,Property
class Mixer(QObject):
    changed=Signal()
    def __init__(self,player,audio,db,parent=None):
        super().__init__(parent); self.player=player; self.audio=audio; self.db=db
        self._speed=1.0; self._balance=0.0; self._gain=1.0; self._preset="Normal"
        self._eq={"bass":0.0,"mid":0.0,"treble":0.0}
    @Property(float,notify=changed)
    def speed(self): return self._speed
    @Property(float,notify=changed)
    def balance(self): return self._balance
    @Property(float,notify=changed)
    def gain(self): return self._gain
    @Slot(float)
    def setSpeed(self,v): self._speed=max(.5,min(2,float(v))); self.player.setPlaybackRate(self._speed); self.changed.emit()
    @Slot(float)
    def setBalance(self,v):
        self._balance=max(-1,min(1,float(v)))
        try: self.audio.setBalance(self._balance)
        except AttributeError: pass
        self.changed.emit()
    @Slot(float)
    def setGain(self,v):
        self._gain=max(.25,min(1.25,float(v)))
        self.audio.setVolume(min(1.0,self._gain)); self.changed.emit()
    @Slot()
    def resetSpeed(self): self.setSpeed(1)
    @Slot()
    def resetBalance(self): self.setBalance(0)
    @Slot()
    def resetGain(self): self.setGain(1)
    @Slot(str)
    def preset(self,name):
        self._preset=name
        profiles={"Normal":(0,0,0),"Bass Boost":(6,1,0),"Vocal":(-1,5,2),"Rock":(4,2,4),"Pop":(2,3,2)}
        b,m,t=profiles.get(name,(0,0,0)); self._eq={"bass":b,"mid":m,"treble":t}
        self.db.set_setting("mixer_preset",name); self.changed.emit()
    @Property(str,notify=changed)
    def presetName(self): return self._preset
